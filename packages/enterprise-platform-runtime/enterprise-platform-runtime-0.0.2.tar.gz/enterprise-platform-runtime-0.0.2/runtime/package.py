from typing import Optional

from pydantic import BaseModel


class PackageGraphNode(BaseModel):
    id: str
    use: Optional[str] = None
    type: str
    method: Optional[str] = None


class PackageGraphEdge(BaseModel):
    id: str
    source: str
    target: str


class PackageGraph(BaseModel):
    nodes: list[PackageGraphNode]
    edges: list[PackageGraphEdge]


class Package(BaseModel):
    id: str
    graph: PackageGraph

    def get_node(self, node_id: str) -> PackageGraphNode:
        return {node.id: node for node in self.graph.nodes}[node_id]
