__author__ = 'varun'

from django.db import models
from django.contrib.auth.models import User
from NetworkAlignment.settings import ALIGNMENT_TASK
from NetworkProperties.settings import NETWORK_PROPERTIES_TASK
from PairwiseAnalysis.settings import PAIRWISE_ANALYSIS_TASK
from DataVsModelAnalysis.settings import DATA_VS_MODEL_TASK
# from CanonicalCorrelationAnalysis.settings import CANONICAL_CORRELATION_TASK
from DataFusion.settings import DATA_FUSION_TASK
from DirectedNetworkProperties.settings import DIRECTED_NETWORK_PROPERTIES_TASK
from DirectedNetworkPairwise.settings import DIRECTED_NETWORK_PAIRWISE_TASK
from DirectedNetworkDataVsModel.settings import DIRECTED_NETWORK_DVM_TASK
from MultipleAlignment.settings import MULTIPLE_ALIGNMENT_TASK
from ProbabilisticNetworksProperties.settings import PROBABILISTIC_NETWORKS_PROPS_TASK
from HyperGraphletsProperties.settings import HYPER_GRAPHLETS_PROPS_TASK
from SimpletsProperties.settings import SIMPLETS_PROPERTIES_TASK
from ProbabilisticNetworksNetAnalysis.settings import PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK
from ProbabilisticNetworksModelAnalysis.settings import PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK
from SimpletsPairwiseAnalysis.settings import SIMPLETS_PAIRWISE_ANALYSIS_TASK
from SimpletsPairwiseAnalysis.settings import SIMPLETS_DVM_ANALYSIS_TASK
from HyperGraphletsNetAnalysis.settings import HYPERGRAPHLETS_NET_ANALYSIS_TASK
from ClusteringAndEnrichment.settings import CLUSTERING_ANALYSIS_TASK
from ClusteringAndEnrichment.settings import ENRICHMENT_ANALYSIS_TASK
from TopologicalAnalysis.settings import TOPOLOGICAL_ANALYSIS_TASK
# flag:NewTaskTemplate
from a_NewTaskTemplate.settings import NEWTASKTEMPLATE_TASK

TASK_TYPES = (
    (ALIGNMENT_TASK, ALIGNMENT_TASK),
    (NETWORK_PROPERTIES_TASK, NETWORK_PROPERTIES_TASK),
    (PAIRWISE_ANALYSIS_TASK, PAIRWISE_ANALYSIS_TASK),
    (DATA_VS_MODEL_TASK, DATA_VS_MODEL_TASK),
    # (CANONICAL_CORRELATION_TASK, CANONICAL_CORRELATION_TASK),
    (DATA_FUSION_TASK, DATA_FUSION_TASK),
    (DIRECTED_NETWORK_PROPERTIES_TASK, DIRECTED_NETWORK_PROPERTIES_TASK),
    (DIRECTED_NETWORK_PAIRWISE_TASK, DIRECTED_NETWORK_PAIRWISE_TASK),
    (DIRECTED_NETWORK_DVM_TASK, DIRECTED_NETWORK_DVM_TASK),
    (MULTIPLE_ALIGNMENT_TASK, MULTIPLE_ALIGNMENT_TASK),
    (PROBABILISTIC_NETWORKS_PROPS_TASK, PROBABILISTIC_NETWORKS_PROPS_TASK),
    (HYPER_GRAPHLETS_PROPS_TASK, HYPER_GRAPHLETS_PROPS_TASK),
    (SIMPLETS_PROPERTIES_TASK, SIMPLETS_PROPERTIES_TASK),
    (PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK, PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK),
    (PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK, PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK),
    (SIMPLETS_PAIRWISE_ANALYSIS_TASK, SIMPLETS_PAIRWISE_ANALYSIS_TASK),
    (SIMPLETS_DVM_ANALYSIS_TASK, SIMPLETS_DVM_ANALYSIS_TASK),
    (HYPERGRAPHLETS_NET_ANALYSIS_TASK, HYPERGRAPHLETS_NET_ANALYSIS_TASK),
    (CLUSTERING_ANALYSIS_TASK, CLUSTERING_ANALYSIS_TASK),
    (ENRICHMENT_ANALYSIS_TASK, ENRICHMENT_ANALYSIS_TASK),
    (TOPOLOGICAL_ANALYSIS_TASK, TOPOLOGICAL_ANALYSIS_TASK),
    # flag:NewTaskTemplate
    (NEWTASKTEMPLATE_TASK, NEWTASKTEMPLATE_TASK),
)


class Task(models.Model):
    taskId = models.AutoField('Task ID', primary_key=True)
    taskName = models.CharField('Task Name', max_length=100)
    user = models.ForeignKey(User, related_name="User")
    finished = models.BooleanField('Task Finished', default=False)
    error_occurred = models.BooleanField('Error Occurred', default=False)
    task_type = models.CharField('Task Type', max_length=100, choices=TASK_TYPES, default="")
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    operational_directory = models.CharField('Operational Directory', max_length=100)
    error_text = models.TextField("Error Text", blank=True, default="")

    def __str__(self):
        return str(self.taskId) + ": " + self.taskName

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return self.__str__()