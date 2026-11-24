"""Capacity Estimation and Back-of-the-Envelope Calculation Engine.

Calculates traffic volume, storage growth, network bandwidth, cache sizing,
and queue throughput based on explicit assumptions and workload parameters.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TrafficProfile:
    """Workload and traffic parameters."""
    daily_active_users: int = 100_000
    monthly_active_users: int = 1_000_000
    actions_per_user_per_day: int = 20
    read_to_write_ratio: float = 10.0  # 10:1 read-heavy default
    avg_read_payload_bytes: int = 4_096   # 4 KB
    avg_write_payload_bytes: int = 2_048  # 2 KB
    peak_surge_multiplier: float = 3.0    # Peak is 3x average
    seconds_per_day: int = 86_400


@dataclass
class StorageEstimate:
    """Calculated storage requirements."""
    daily_raw_bytes: int
    daily_raw_gb: float
    annual_raw_tb: float
    replication_factor: int
    annual_replicated_tb: float
    index_overhead_percent: float
    annual_total_provisioned_tb: float
    five_year_total_tb: float


@dataclass
class BandwidthEstimate:
    """Calculated network bandwidth throughput."""
    avg_ingress_mbps: float
    peak_ingress_mbps: float
    avg_egress_mbps: float
    peak_egress_mbps: float
    monthly_egress_tb: float


@dataclass
class CacheEstimate:
    """Calculated memory and cache sizing."""
    daily_read_volume_bytes: int
    cache_working_set_percent: float  # typically 20% for 80/20 Pareto
    raw_cache_ram_gb: float
    eviction_overhead_factor: float
    recommended_cache_ram_gb: float
    recommended_nodes: int


@dataclass
class QueueEstimate:
    """Calculated message queue throughput and worker concurrency."""
    avg_writes_per_sec: float
    peak_writes_per_sec: float
    single_worker_throughput_wps: float
    min_worker_concurrency: int
    peak_worker_concurrency: int
    surge_buffer_storage_mb: float


@dataclass
class ComprehensiveCapacityReport:
    """Unified capacity estimation report."""
    traffic: TrafficProfile
    avg_rps: float
    peak_rps: float
    avg_read_qps: float
    peak_read_qps: float
    avg_write_wps: float
    peak_write_wps: float
    storage: StorageEstimate
    bandwidth: BandwidthEstimate
    cache: CacheEstimate
    queue: QueueEstimate

    def to_markdown(self) -> str:
        """Render a clean GitHub-flavored markdown capacity report."""
        lines = [
            "# System Capacity & Sizing Estimation Report",
            "",
            "## 1. Traffic & Request Rates",
            f"- **Daily Active Users (DAU):** {self.traffic.daily_active_users:,}",
            f"- **Monthly Active Users (MAU):** {self.traffic.monthly_active_users:,}",
            f"- **Actions / Day / User:** {self.traffic.actions_per_user_per_day}",
            f"- **Read : Write Ratio:** {self.traffic.read_to_write_ratio:.1f} : 1",
            f"- **Average Overall RPS:** {self.avg_rps:,.2f} req/s",
            f"- **Peak Overall RPS (surge {self.traffic.peak_surge_multiplier:.1f}x):** {self.peak_rps:,.2f} req/s",
            f"- **Read QPS:** Avg {self.avg_read_qps:,.2f} / Peak {self.peak_read_qps:,.2f}",
            f"- **Write WPS:** Avg {self.avg_write_wps:,.2f} / Peak {self.peak_write_wps:,.2f}",
            "",
            "## 2. Storage Requirements",
            f"- **Daily Raw Storage:** {self.storage.daily_raw_gb:.2f} GB/day",
            f"- **Annual Raw Storage:** {self.storage.annual_raw_tb:.2f} TB/year",
            f"- **Replication Factor:** {self.storage.replication_factor}x",
            f"- **Annual Replicated Storage:** {self.storage.annual_replicated_tb:.2f} TB/year",
            f"- **Index & Metadata Overhead:** +{self.storage.index_overhead_percent:.0f}%",
            f"- **Annual Provisioned Storage:** {self.storage.annual_total_provisioned_tb:.2f} TB",
            f"- **5-Year Growth Projection:** {self.storage.five_year_total_tb:.2f} TB",
            "",
            "## 3. Network Bandwidth",
            f"- **Ingress (Writes/Uploads):** Avg {self.bandwidth.avg_ingress_mbps:.2f} Mbps | Peak {self.bandwidth.peak_ingress_mbps:.2f} Mbps",
            f"- **Egress (Reads/Downloads):** Avg {self.bandwidth.avg_egress_mbps:.2f} Mbps | Peak {self.bandwidth.peak_egress_mbps:.2f} Mbps",
            f"- **Monthly Egress Data Transfer:** {self.bandwidth.monthly_egress_tb:.2f} TB/month",
            "",
            "## 4. Caching Sizing (Pareto 80/20 Rule)",
            f"- **Working Set Ratio:** {self.cache.cache_working_set_percent * 100:.0f}% of daily read volume",
            f"- **Raw Cache RAM Required:** {self.cache.raw_cache_ram_gb:.2f} GB",
            f"- **Recommended Provisioned RAM (inc overhead):** {self.cache.recommended_cache_ram_gb:.2f} GB",
            f"- **Recommended Cache Topology:** {self.cache.recommended_nodes} nodes (Redis Cluster / Sentinel)",
            "",
            "## 5. Async Processing & Queue Sizing",
            f"- **Peak Queue Ingestion Rate:** {self.queue.peak_writes_per_sec:,.2f} msg/s",
            f"- **Min Workers (steady state):** {self.queue.min_worker_concurrency} workers",
            f"- **Peak Auto-scaled Workers:** {self.queue.peak_worker_concurrency} workers",
            f"- **1-Hour Peak Surge Buffer:** {self.queue.surge_buffer_storage_mb:.2f} MB",
        ]
        return "\n".join(lines)


class CapacityEstimator:
    """Deterministic capacity calculation engine."""

    def __init__(
        self,
        replication_factor: int = 3,
        index_overhead_percent: float = 25.0,
        cache_working_set_percent: float = 0.20,
        cache_overhead_factor: float = 1.30,
        single_worker_throughput_wps: float = 50.0,
    ):
        self.replication_factor = replication_factor
        self.index_overhead_percent = index_overhead_percent
        self.cache_working_set_percent = cache_working_set_percent
        self.cache_overhead_factor = cache_overhead_factor
        self.single_worker_throughput_wps = single_worker_throughput_wps

    def estimate(self, profile: TrafficProfile) -> ComprehensiveCapacityReport:
        """Run back-of-the-envelope calculations for the given profile."""
        total_daily_actions = profile.daily_active_users * profile.actions_per_user_per_day
        avg_rps = total_daily_actions / profile.seconds_per_day
        peak_rps = avg_rps * profile.peak_surge_multiplier

        # Decompose read vs write
        # read_ratio : write_ratio = R : 1
        # fraction_writes = 1 / (R + 1)
        # fraction_reads = R / (R + 1)
        denom = profile.read_to_write_ratio + 1.0
        fraction_writes = 1.0 / denom
        fraction_reads = profile.read_to_write_ratio / denom

        avg_read_qps = avg_rps * fraction_reads
        peak_read_qps = peak_rps * fraction_reads

        avg_write_wps = avg_rps * fraction_writes
        peak_write_wps = peak_rps * fraction_writes

        # Storage
        daily_write_count = total_daily_actions * fraction_writes
        daily_raw_bytes = int(daily_write_count * profile.avg_write_payload_bytes)
        daily_raw_gb = daily_raw_bytes / (1024 ** 3)
        annual_raw_tb = (daily_raw_gb * 365) / 1024
        annual_replicated_tb = annual_raw_tb * self.replication_factor
        overhead_multiplier = 1.0 + (self.index_overhead_percent / 100.0)
        annual_total_provisioned_tb = annual_replicated_tb * overhead_multiplier
        five_year_total_tb = annual_total_provisioned_tb * 5.0

        storage = StorageEstimate(
            daily_raw_bytes=daily_raw_bytes,
            daily_raw_gb=daily_raw_gb,
            annual_raw_tb=annual_raw_tb,
            replication_factor=self.replication_factor,
            annual_replicated_tb=annual_replicated_tb,
            index_overhead_percent=self.index_overhead_percent,
            annual_total_provisioned_tb=annual_total_provisioned_tb,
            five_year_total_tb=five_year_total_tb,
        )

        # Bandwidth
        # Ingress = writes * write payload
        # Egress = reads * read payload
        avg_ingress_bytes_sec = avg_write_wps * profile.avg_write_payload_bytes
        peak_ingress_bytes_sec = peak_write_wps * profile.avg_write_payload_bytes
        avg_ingress_mbps = (avg_ingress_bytes_sec * 8) / 1_000_000
        peak_ingress_mbps = (peak_ingress_bytes_sec * 8) / 1_000_000

        avg_egress_bytes_sec = avg_read_qps * profile.avg_read_payload_bytes
        peak_egress_bytes_sec = peak_read_qps * profile.avg_read_payload_bytes
        avg_egress_mbps = (avg_egress_bytes_sec * 8) / 1_000_000
        peak_egress_mbps = (peak_egress_bytes_sec * 8) / 1_000_000

        monthly_egress_bytes = avg_egress_bytes_sec * profile.seconds_per_day * 30.5
        monthly_egress_tb = monthly_egress_bytes / (1024 ** 4)

        bandwidth = BandwidthEstimate(
            avg_ingress_mbps=avg_ingress_mbps,
            peak_ingress_mbps=peak_ingress_mbps,
            avg_egress_mbps=avg_egress_mbps,
            peak_egress_mbps=peak_egress_mbps,
            monthly_egress_tb=monthly_egress_tb,
        )

        # Cache Sizing
        daily_read_count = total_daily_actions * fraction_reads
        daily_read_volume_bytes = int(daily_read_count * profile.avg_read_payload_bytes)
        working_set_bytes = daily_read_volume_bytes * self.cache_working_set_percent
        raw_cache_ram_gb = working_set_bytes / (1024 ** 3)
        recommended_cache_ram_gb = raw_cache_ram_gb * self.cache_overhead_factor
        # Sizing nodes: assume 32 GB or 64 GB max per node for cluster management
        recommended_nodes = max(2, math.ceil(recommended_cache_ram_gb / 32.0))

        cache = CacheEstimate(
            daily_read_volume_bytes=daily_read_volume_bytes,
            cache_working_set_percent=self.cache_working_set_percent,
            raw_cache_ram_gb=raw_cache_ram_gb,
            eviction_overhead_factor=self.cache_overhead_factor,
            recommended_cache_ram_gb=recommended_cache_ram_gb,
            recommended_nodes=recommended_nodes,
        )

        # Queue Sizing
        min_workers = max(1, math.ceil(avg_write_wps / self.single_worker_throughput_wps))
        peak_workers = max(min_workers, math.ceil(peak_write_wps / self.single_worker_throughput_wps))
        # 1-hour buffer size at peak rate
        one_hour_bytes = peak_write_wps * profile.avg_write_payload_bytes * 3600
        surge_buffer_mb = one_hour_bytes / (1024 ** 2)

        queue = QueueEstimate(
            avg_writes_per_sec=avg_write_wps,
            peak_writes_per_sec=peak_write_wps,
            single_worker_throughput_wps=self.single_worker_throughput_wps,
            min_worker_concurrency=min_workers,
            peak_worker_concurrency=peak_workers,
            surge_buffer_storage_mb=surge_buffer_mb,
        )

        return ComprehensiveCapacityReport(
            traffic=profile,
            avg_rps=avg_rps,
            peak_rps=peak_rps,
            avg_read_qps=avg_read_qps,
            peak_read_qps=peak_read_qps,
            avg_write_wps=avg_write_wps,
            peak_write_wps=peak_write_wps,
            storage=storage,
            bandwidth=bandwidth,
            cache=cache,
            queue=queue,
        )
