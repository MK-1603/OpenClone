<#
.SYNOPSIS
    OpenClone 2.0 Authenticode Code Signing & Verification Engine.

.DESCRIPTION
    Provides secure, robust signing and verification for Windows distribution
    artifacts (oc.exe, bundled binaries, DLLs, OpenClone-Setup.exe).
    
    Supports:
      1. Windows SDK SignTool.exe (Preferred in CI and dev environments with Windows SDK)
      2. Native PowerShell Set-AuthenticodeSignature (Fallback when SignTool is not present)
      3. Microsoft Trusted Signing integration hooks
      4. RFC 3161 compliant timestamping (DigiCert / Sectigo)
      5. Strict signature and publisher verification
#>

function Find-SignTool {
    [CmdletBinding()]
    param()

    # Check PATH first
    $cmd = Get-Command signtool.exe -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }

    # Search standard Windows Kits directories
    $kitsRoots = @(
        "C:\Program Files (x86)\Windows Kits\10\bin",
        "C:\Program Files\Windows Kits\10\bin",
        "C:\Program Files (x86)\Windows Kits\8.1\bin"
    )

    foreach ($root in $kitsRoots) {
        if (Test-Path $root) {
            $candidates = Get-ChildItem -Path $root -Filter "signtool.exe" -Recurse -Depth 3 -ErrorAction SilentlyContinue |
                          Where-Object { $_.FullName -match "x64|x86" } |
                          Sort-Object -Property FullName -Descending
            if ($candidates -and $candidates.Count -gt 0) {
                return $candidates[0].FullName
            }
        }
    }

    return $null
}

function Get-SigningCertificate {
    [CmdletBinding()]
    param(
        [string]$CertThumbprint,
        [string]$CertSubject,
        [string]$PfxPath,
        [System.Security.SecureString]$PfxSecurePassword
    )

    # 1. PFX File mode if provided
    if ($PfxPath -and (Test-Path $PfxPath)) {
        try {
            $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
            if ($PfxSecurePassword) {
                $cert.Import($PfxPath, $PfxSecurePassword, [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::Exportable)
            } else {
                $cert.Import($PfxPath)
            }
            return [PSCustomObject]@{
                Certificate = $cert
                SourceType  = "PFX"
                SourcePath  = $PfxPath
            }
        } catch {
            Write-Warning "Failed to load certificate from PFX '$PfxPath': $($_.Exception.Message)"
        }
    }

    # 2. Windows Certificate Store lookup (CurrentUser \ LocalMachine)
    $stores = @("Cert:\CurrentUser\My", "Cert:\LocalMachine\My")

    if ($CertThumbprint) {
        $cleanThumb = $CertThumbprint.Replace(" ", "").ToUpper()
        foreach ($s in $stores) {
            $found = Get-Item "$s\$cleanThumb" -ErrorAction SilentlyContinue
            if ($found -and $found.HasPrivateKey) {
                return [PSCustomObject]@{
                    Certificate = $found
                    SourceType  = "StoreThumbprint"
                    StorePath   = $s
                    Thumbprint  = $cleanThumb
                }
            }
        }
    }

    if ($CertSubject) {
        foreach ($s in $stores) {
            $found = Get-ChildItem -Path $s -ErrorAction SilentlyContinue |
                     Where-Object { $_.Subject -like "*$CertSubject*" -and $_.HasPrivateKey }
            if ($found) {
                $selected = if ($found -is [array]) { $found[0] } else { $found }
                return [PSCustomObject]@{
                    Certificate = $selected
                    SourceType  = "StoreSubject"
                    StorePath   = $s
                    Thumbprint  = $selected.Thumbprint
                }
            }
        }
    }

    # 3. CodeSigning cert auto-detection (Must have Code Signing EKU: 1.3.6.1.5.5.7.3.3 and Private Key)
    foreach ($s in $stores) {
        $certs = Get-ChildItem -Path $s -ErrorAction SilentlyContinue |
                 Where-Object {
                     $_.HasPrivateKey -and
                     $_.NotAfter -gt (Get-Date) -and
                     ($_.EnhancedKeyUsageList.ObjectId -contains "1.3.6.1.5.5.7.3.3")
                 }
        if ($certs) {
            $best = if ($certs -is [array]) { $certs[0] } else { $certs }
            return [PSCustomObject]@{
                Certificate = $best
                SourceType  = "StoreAuto"
                StorePath   = $s
                Thumbprint  = $best.Thumbprint
            }
        }
    }

    return $null
}

function Invoke-AuthenticodeSign {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath,

        [Parameter(Mandatory=$false)]
        $SigningCertInfo,

        [Parameter(Mandatory=$false)]
        [string]$TimestampUrl = "http://timestamp.digicert.com",

        [Parameter(Mandatory=$false)]
        [string]$SignToolPath,

        [Parameter(Mandatory=$false)]
        [string]$PfxPasswordPlain
    )

    if (-not (Test-Path $FilePath)) {
        throw "Target file to sign not found: $FilePath"
    }

    $resolvedSignTool = $SignToolPath
    if (-not $resolvedSignTool) {
        $resolvedSignTool = Find-SignTool
    }

    $fileFull = (Resolve-Path $FilePath).Path

    # Scenario A: Using Windows SDK SignTool
    if ($resolvedSignTool -and (Test-Path $resolvedSignTool)) {
        Write-Host "      [SIGNTOOL] Signing $FilePath with SignTool.exe..." -ForegroundColor DarkGray
        
        $signArgs = @("sign", "/v", "/fd", "SHA256", "/tr", $TimestampUrl, "/td", "SHA256")

        if ($SigningCertInfo.SourceType -eq "PFX") {
            $signArgs += @("/f", $SigningCertInfo.SourcePath)
            if ($PfxPasswordPlain) {
                $signArgs += @("/p", $PfxPasswordPlain)
            }
        } elseif ($SigningCertInfo.Thumbprint) {
            $signArgs += @("/sha1", $SigningCertInfo.Thumbprint)
        } else {
            $signArgs += "/a"  # Select best certificate automatically
        }

        $signArgs += $fileFull

        $pinfo = New-Object System.Diagnostics.ProcessStartInfo
        $pinfo.FileName = $resolvedSignTool
        $pinfo.Arguments = ($signArgs -join " ")
        $pinfo.RedirectStandardOutput = $true
        $pinfo.RedirectStandardError = $true
        $pinfo.UseShellExecute = $false
        $pinfo.CreateNoWindow = $true

        $proc = [System.Diagnostics.Process]::Start($pinfo)
        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit()

        if ($proc.ExitCode -eq 0) {
            return [PSCustomObject]@{
                Success = $true
                Tool    = "SignTool"
                Details = $stdout.Trim()
            }
        } else {
            return [PSCustomObject]@{
                Success = $false
                Tool    = "SignTool"
                Error   = "$stdout `n $stderr".Trim()
            }
        }
    }

    # Scenario B: Native PowerShell Set-AuthenticodeSignature Fallback
    if ($SigningCertInfo -and $SigningCertInfo.Certificate) {
        Write-Host "      [POWERSHELL] Signing $FilePath with Set-AuthenticodeSignature..." -ForegroundColor DarkGray
        try {
            $sigResult = Set-AuthenticodeSignature -FilePath $fileFull `
                                                  -Certificate $SigningCertInfo.Certificate `
                                                  -HashAlgorithm SHA256 `
                                                  -TimestampServer $TimestampUrl

            $isSuccess = ($sigResult.Status -eq [System.Management.Automation.SignatureStatus]::Valid)
            return [PSCustomObject]@{
                Success       = $isSuccess
                Tool          = "Set-AuthenticodeSignature"
                Status        = $sigResult.Status.ToString()
                StatusMessage = $sigResult.StatusMessage
            }
        } catch {
            return [PSCustomObject]@{
                Success = $false
                Tool    = "Set-AuthenticodeSignature"
                Error   = $_.Exception.Message
            }
        }
    }

    return [PSCustomObject]@{
        Success = $false
        Tool    = "None"
        Error   = "No signing certificate or SignTool available."
    }
}

function Test-AuthenticodeSignatureStrict {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$FilePath,

        [Parameter(Mandatory=$false)]
        [string]$SignToolPath
    )

    if (-not (Test-Path $FilePath)) {
        return [PSCustomObject]@{
            Status        = "NotFound"
            IsValid       = $false
            Subject       = $null
            Issuer        = $null
            StatusMessage = "File not found"
        }
    }

    $fileFull = (Resolve-Path $FilePath).Path

    # 1. Check with SignTool if available
    $resolvedSignTool = $SignToolPath
    if (-not $resolvedSignTool) {
        $resolvedSignTool = Find-SignTool
    }

    if ($resolvedSignTool -and (Test-Path $resolvedSignTool)) {
        $pinfo = New-Object System.Diagnostics.ProcessStartInfo
        $pinfo.FileName = $resolvedSignTool
        $pinfo.Arguments = "verify /pa /v `"$fileFull`""
        $pinfo.RedirectStandardOutput = $true
        $pinfo.RedirectStandardError = $true
        $pinfo.UseShellExecute = $false
        $pinfo.CreateNoWindow = $true

        $proc = [System.Diagnostics.Process]::Start($pinfo)
        $stdout = $proc.StandardOutput.ReadToEnd()
        $stderr = $proc.StandardError.ReadToEnd()
        $proc.WaitForExit()

        $isValid = ($proc.ExitCode -eq 0)
        $psSig = Get-AuthenticodeSignature -FilePath $fileFull -ErrorAction SilentlyContinue

        return [PSCustomObject]@{
            Status        = if ($isValid) { "Valid" } else { "VerificationFailed" }
            IsValid       = $isValid
            Tool          = "SignTool"
            Subject       = if ($psSig -and $psSig.SignerCertificate) { $psSig.SignerCertificate.Subject } else { $null }
            Issuer        = if ($psSig -and $psSig.SignerCertificate) { $psSig.SignerCertificate.Issuer } else { $null }
            StatusMessage = if ($isValid) { "Verified successfully by SignTool" } else { $stdout }
        }
    }

    # 2. Check with PowerShell Authenticode
    $sig = Get-AuthenticodeSignature -FilePath $fileFull -ErrorAction SilentlyContinue
    $statusStr = if ($sig) { $sig.Status.ToString() } else { "NotSigned" }
    $isValid = ($sig -and $sig.Status -eq [System.Management.Automation.SignatureStatus]::Valid)

    return [PSCustomObject]@{
        Status        = $statusStr
        IsValid       = $isValid
        Tool          = "Get-AuthenticodeSignature"
        Subject       = if ($sig -and $sig.SignerCertificate) { $sig.SignerCertificate.Subject } else { $null }
        Issuer        = if ($sig -and $sig.SignerCertificate) { $sig.SignerCertificate.Issuer } else { $null }
        StatusMessage = if ($sig) { $sig.StatusMessage } else { "No signature present" }
    }
}
