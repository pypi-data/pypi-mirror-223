"""Implementation of mcli describe cluster"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, Generator, List, Optional, Tuple

from rich import print as rprint
from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from mcli.api.cluster.api_get_clusters import get_clusters
from mcli.api.exceptions import MAPIException, cli_error_handler
from mcli.api.model.cluster_details import ClusterDetails, Instance, Node
from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay, create_vertical_display_table
from mcli.utils.utils_logging import FormatString, format_string

logger = logging.getLogger(__name__)


class DescribeClusterDetailColumns(Enum):
    NAME = 'name'
    ID = 'cluster_id'
    ALLOWED_SUBMISSION_TYPES = 'allowed_submission_types'
    PROVIDER = 'provider'
    IS_MULTITENANT = 'is_multitenant'
    SCHEDULER_ENABLED = 'scheduler_enabled'
    IS_MULTINODE = 'is_multinode'
    ALLOW_FRACTIONAL = 'allow_fractional'


CLUSTER_DETAIL_DISPLAY_NAMES = [
    'Name', 'ID', 'Allowed Submission Types', 'Cloud Provider', 'Is Multitenant', 'Priority and Preemption Enabled',
    'Multinode Training Enabled', 'Fractional Training Enabled'
]


class NodeColumns(Enum):
    NAME = "name"
    INSTANCE = "instance"
    STATUS = "status"
    SCHEDULABLE = "schedulable"


@dataclass
class DescribeClusterDetailDisplayItem(MCLIDisplayItem):
    """Tuple that extracts detailed run data for display purposes"""
    name: str
    cluster_id: str
    allowed_submission_types: str
    provider: str
    is_multitenant: bool
    scheduler_enabled: bool
    is_multinode: bool
    allow_fractional: bool

    @classmethod
    def from_cluster(cls, cluster: ClusterDetails) -> DescribeClusterDetailDisplayItem:
        submission_types = ', '.join([sub_type.name.lower().capitalize() for sub_type in cluster.submission_types])
        extracted: Dict[str, Any] = {
            DescribeClusterDetailColumns.NAME.value: cluster.name,
            DescribeClusterDetailColumns.ID.value: cluster.id,
            DescribeClusterDetailColumns.ALLOWED_SUBMISSION_TYPES.value: submission_types,
            DescribeClusterDetailColumns.PROVIDER.value: cluster.provider,
            DescribeClusterDetailColumns.IS_MULTITENANT.value: cluster.is_multitenant,
            DescribeClusterDetailColumns.SCHEDULER_ENABLED.value: cluster.scheduler_enabled,
            DescribeClusterDetailColumns.IS_MULTINODE.value: cluster.allow_multinode,
            DescribeClusterDetailColumns.ALLOW_FRACTIONAL.value: cluster.allow_fractional,
        }
        return DescribeClusterDetailDisplayItem(**extracted)


class MCLIDescribeClusterDetailsDisplay(MCLIGetDisplay):
    """ Vertical table view of cluster details """

    def __init__(self, models: List[ClusterDetails]):
        self.models = models

    @property
    def index_label(self) -> str:
        return ""

    def create_custom_table(self, columns: List[str], data: List[Tuple[Any, ...]], names: List[str]) -> Optional[Table]:
        column_names = CLUSTER_DETAIL_DISPLAY_NAMES
        return create_vertical_display_table(data=data, columns=column_names)

    def __iter__(self) -> Generator[DescribeClusterDetailDisplayItem, None, None]:
        for model in self.models:
            item = DescribeClusterDetailDisplayItem.from_cluster(model)
            yield item


class MCLIInstanceDisplay():
    """ Panel view of instance details """

    def __init__(self, model: List[Instance]):
        self.model = model

    def print(self):
        # Build the visual panels for Instance details
        all_columns = []
        curr_columns = []
        count = 0
        total_gpus = sum(instance.gpus * instance.nodes for instance in self.model)
        total_nodes = sum(instance.nodes for instance in self.model)
        total_cpus = sum(instance.cpus for instance in self.model if instance.cpus is not None)
        print(f'Total Nodes: {total_nodes}')
        print(f'Total GPUs: {total_gpus}')
        print(f'Total CPUs: {total_cpus}')

        for instance in self.model:
            if count % 3 == 0 and count != 0:
                all_columns.append(Columns(curr_columns))
                curr_columns = [create_instance_panel(instance)]
            else:
                curr_columns.append(create_instance_panel(instance))
            count += 1
        all_columns.append(Columns(curr_columns))

        for col in all_columns:
            rprint(col)
            print()


def create_instance_panel(instance: Instance) -> Panel:
    """ Creates a panel for instance details """
    if len(instance.name) > 20:
        instance.name = instance.name[:17] + "..."
    instance_details = f"[bold]Instance Name: [/bold]{instance.name}\n[bold]GPU Type: [/bold]{instance.gpu_type}"
    gpu_string = f"GPUs: {instance.gpus*instance.nodes}"
    nodes = instance.nodes
    node_string = f"Nodes: {nodes}"
    per_node = "\n\n\n"
    storage_per_node = f"Storage: {instance.storage}"
    memory_per_node = f"RAM: {instance.memory}"
    per_node = f"[bold]Per Node: [/bold]\nGPUs: {instance.gpus}\n{storage_per_node}\n{memory_per_node}"
    return Panel(f"{instance_details}\n\n{node_string}\n{gpu_string}\n\n{per_node}", expand=True, width=40)


@dataclass
class NodeDisplayItem(MCLIDisplayItem):
    """Tuple that extracts run data for display purposes.
    """
    name: str
    instance: str
    status: str
    schedulable: str

    @classmethod
    def from_node(cls, node: Node, instance: str) -> NodeDisplayItem:
        extracted: Dict[str, str] = {}
        extracted[NodeColumns.NAME.value] = node.name
        extracted[NodeColumns.INSTANCE.value] = instance
        extracted[NodeColumns.STATUS.value] = "Alive" if node.is_alive else "Dead"
        extracted[NodeColumns.SCHEDULABLE.value] = str(node.is_schedulable)

        return NodeDisplayItem(**extracted)


class MCLIInstanceNodeDisplay(MCLIGetDisplay):
    """Display manager for nodes
    """

    def __init__(self, models: List[Instance]):
        self.models = models

    @property
    def override_column_ordering(self) -> Optional[List[str]]:
        return [col.value for col in NodeColumns if col != NodeColumns.NAME]

    def __iter__(self) -> Generator[NodeDisplayItem, None, None]:
        for model in self.models:
            for node in model.node_details:
                item = NodeDisplayItem.from_node(node=node, instance=model.name)
                yield item


@cli_error_handler("mcli describe cluster")
def describe_cluster(cluster_name: str | None, output: OutputDisplay = OutputDisplay.TABLE, **kwargs):
    """
    Fetches more details of a Cluster
    """
    del kwargs

    cluster = get_clusters()
    if cluster_name is None and len(cluster) > 1:
        raise MAPIException(
            HTTPStatus.BAD_REQUEST,
            f'Multiple clusters found. Please specify one of the following: {", ".join([c.name for c in cluster])}',
        )

    if cluster_name is not None:
        cluster = get_clusters(clusters=[cluster_name])

    if not cluster:
        raise MAPIException(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f'Cluster {cluster_name} not found.',
        )

    # Cluster details section
    print(format_string('Cluster Details', FormatString.BOLD))
    cluster_details_display = MCLIDescribeClusterDetailsDisplay(cluster)
    cluster_details_display.print(output)
    print()

    # Instance details section
    instances = cluster[0].cluster_instances
    instance_display = MCLIInstanceDisplay(instances)
    instance_display.print()
    print()

    # Node details section
    print(format_string('Node Details', FormatString.BOLD))
    display = MCLIInstanceNodeDisplay(instances)
    display.print(output)
