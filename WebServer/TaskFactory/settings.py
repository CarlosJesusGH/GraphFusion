__author__ = 'varun'

from NetworkAlignment.settings import ALIGNMENT_TASK
from NetworkProperties.settings import NETWORK_PROPERTIES_TASK
from PairwiseAnalysis.settings import PAIRWISE_ANALYSIS_TASK
from DataVsModelAnalysis.settings import DATA_VS_MODEL_TASK
from CanonicalCorrelationAnalysis.settings import CANONICAL_CORRELATION_TASK
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
from GraphletEigencentralities.settings import GraphletEigencentralities_TASK
from GraphletLaplacians.settings import GraphletLaplacians_TASK
from VisualizeSE.settings import VISUALIZESE_TASK
# flag:NewTaskTemplate
from a_NewTaskTemplate.settings import NEWTASKTEMPLATE_TASK
# ---
from PairwiseAnalysis.views import get_view_for_task as pairwise_analysis_view, \
    delete_data_for_task as pairwise_analysis_delete, get_raw_data_for_task as download_results_pairwise
from NetworkAlignment.views import get_view_for_task as alignment_view, \
    delete_data_for_task as alignment_delete, get_raw_data_for_task as download_results_alignment
from NetworkProperties.views import get_view_for_task as properties_view, \
    delete_data_for_task as network_properties_delete, get_raw_data_for_task as download_properties_result
from DataVsModelAnalysis.views import get_view_for_task as data_vs_model_view, \
    delete_data_for_task as data_vs_model_delete, get_raw_data_for_task as download_data_vs_model_result
from CanonicalCorrelationAnalysis.views import get_view_for_task as canonical_view, \
    get_raw_data_for_task as download_canonical_result, delete_data_for_task as delete_canonical_task
from DataFusion.views import get_view_for_task as data_fusion_view, \
    delete_data_for_task as data_fusion_delete, get_raw_data_for_task as download_data_fusion_result
from DirectedNetworkProperties.views import get_view_for_task as dn_properties_view, \
    delete_data_for_task as dn_network_properties_delete, get_raw_data_for_task as dn_download_properties_result
from DirectedNetworkPairwise.views import get_view_for_task as dn_pairwise_analysis_view, \
    delete_data_for_task as dn_pairwise_analysis_delete, get_raw_data_for_task as dn_download_results_pairwise
from DirectedNetworkDataVsModel.views import get_view_for_task as dn_data_vs_model_view, \
    delete_data_for_task as dn_data_vs_model_delete, get_raw_data_for_task as dn_download_data_vs_model_result
from MultipleAlignment.views import get_view_for_task as MultipleAlignment_view, \
    delete_data_for_task as MultipleAlignment_delete, get_raw_data_for_task as MultipleAlignment_result
from ProbabilisticNetworksProperties.views import get_view_for_task as ProbabilisticNetworksProperties_view, \
    delete_data_for_task as ProbabilisticNetworksProperties_delete, get_raw_data_for_task as ProbabilisticNetworksProperties_result
from HyperGraphletsProperties.views import get_view_for_task as HyperGraphletsProperties_view, \
    delete_data_for_task as HyperGraphletsProperties_delete, get_raw_data_for_task as HyperGraphletsProperties_result
from SimpletsProperties.views import get_view_for_task as SimpletsProperties_view, \
    delete_data_for_task as SimpletsProperties_delete, get_raw_data_for_task as SimpletsProperties_result
from ProbabilisticNetworksNetAnalysis.views import get_view_for_task as ProbabilisticNetworksNetAnalysis_view, \
    delete_data_for_task as ProbabilisticNetworksNetAnalysis_delete, get_raw_data_for_task as ProbabilisticNetworksNetAnalysis_result
from ProbabilisticNetworksModelAnalysis.views import get_view_for_task as ProbabilisticNetworksModelAnalysis_view, \
    delete_data_for_task as ProbabilisticNetworksModelAnalysis_delete, get_raw_data_for_task as ProbabilisticNetworksModelAnalysis_result
from SimpletsPairwiseAnalysis.views import get_view_for_task as SimpletsPairwiseAnalysis_view, \
    delete_data_for_task as SimpletsPairwiseAnalysis_delete, get_raw_data_for_task as SimpletsPairwiseAnalysis_result
from SimpletsPairwiseAnalysis.views import get_view_for_task_dvm as SimpletsDataVsModel_view, \
    delete_data_for_task as SimpletsDataVsModel_delete, get_raw_data_for_task as SimpletsDataVsModel_result
from HyperGraphletsNetAnalysis.views import get_view_for_task as HyperGraphletsNetAnalysis_view, \
    delete_data_for_task as HyperGraphletsNetAnalysis_delete, get_raw_data_for_task as HyperGraphletsNetAnalysis_result
from GraphletEigencentralities.views import get_view_for_task as GraphletEigencentralities_view, \
    delete_data_for_task as GraphletEigencentralities_delete, get_raw_data_for_task as GraphletEigencentralities_result
from GraphletLaplacians.views import get_view_for_task as GraphletLaplacians_view, \
    delete_data_for_task as GraphletLaplacians_delete, get_raw_data_for_task as GraphletLaplacians_result
from VisualizeSE.views import get_view_for_task as VisualizeSE_view, \
    delete_data_for_task as VisualizeSE_delete, get_raw_data_for_task as VisualizeSE_result
# flag:NewTaskTemplate
from a_NewTaskTemplate.views import get_view_for_task as getview_newtasktemplate, \
    delete_data_for_task as deletedata_newtasktemplate, get_raw_data_for_task as getrawdata_newtasktemplate


TASK_TYPES = [PAIRWISE_ANALYSIS_TASK, NETWORK_PROPERTIES_TASK, ALIGNMENT_TASK, DATA_VS_MODEL_TASK,
              CANONICAL_CORRELATION_TASK, DATA_FUSION_TASK, DIRECTED_NETWORK_PROPERTIES_TASK,
              DIRECTED_NETWORK_PAIRWISE_TASK, DIRECTED_NETWORK_DVM_TASK, MULTIPLE_ALIGNMENT_TASK,
              PROBABILISTIC_NETWORKS_PROPS_TASK, HYPER_GRAPHLETS_PROPS_TASK, SIMPLETS_PROPERTIES_TASK,
              PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK, PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK,
              SIMPLETS_PAIRWISE_ANALYSIS_TASK, SIMPLETS_DVM_ANALYSIS_TASK, HYPERGRAPHLETS_NET_ANALYSIS_TASK, GraphletEigencentralities_TASK, GraphletLaplacians_TASK, VISUALIZESE_TASK,
              # flag:NewTaskTemplate
              NEWTASKTEMPLATE_TASK,]

VIEW_FUNCTION_MAPPINGS = {
    PAIRWISE_ANALYSIS_TASK: pairwise_analysis_view,
    NETWORK_PROPERTIES_TASK: properties_view,
    ALIGNMENT_TASK: alignment_view,
    DATA_VS_MODEL_TASK: data_vs_model_view,
    CANONICAL_CORRELATION_TASK: canonical_view,
    DATA_FUSION_TASK: data_fusion_view,
    DIRECTED_NETWORK_PROPERTIES_TASK: dn_properties_view,
    DIRECTED_NETWORK_PAIRWISE_TASK: dn_pairwise_analysis_view,
    DIRECTED_NETWORK_DVM_TASK: dn_data_vs_model_view,
    MULTIPLE_ALIGNMENT_TASK: MultipleAlignment_view,
    PROBABILISTIC_NETWORKS_PROPS_TASK: ProbabilisticNetworksProperties_view,
    HYPER_GRAPHLETS_PROPS_TASK: HyperGraphletsProperties_view,
    SIMPLETS_PROPERTIES_TASK: SimpletsProperties_view,
    PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK: ProbabilisticNetworksNetAnalysis_view,
    PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK: ProbabilisticNetworksModelAnalysis_view,
    SIMPLETS_PAIRWISE_ANALYSIS_TASK: SimpletsPairwiseAnalysis_view,
    SIMPLETS_DVM_ANALYSIS_TASK: SimpletsDataVsModel_view,
    HYPERGRAPHLETS_NET_ANALYSIS_TASK: HyperGraphletsNetAnalysis_view,
    GraphletEigencentralities_TASK: GraphletEigencentralities_view,
    GraphletLaplacians_TASK: GraphletLaplacians_view,
    VISUALIZESE_TASK: VisualizeSE_view,
    # flag:NewTaskTemplate
    NEWTASKTEMPLATE_TASK: getview_newtasktemplate,
}

DOWNLOAD_RESULTS_FUNCTIONS = {
    ALIGNMENT_TASK: download_results_alignment,
    PAIRWISE_ANALYSIS_TASK: download_results_pairwise,
    NETWORK_PROPERTIES_TASK: download_properties_result,
    DATA_VS_MODEL_TASK: download_data_vs_model_result,
    CANONICAL_CORRELATION_TASK: download_canonical_result,
    DATA_FUSION_TASK: download_data_fusion_result,
    DIRECTED_NETWORK_PROPERTIES_TASK: dn_download_properties_result,
    DIRECTED_NETWORK_PAIRWISE_TASK: dn_download_results_pairwise,
    DIRECTED_NETWORK_DVM_TASK: dn_download_data_vs_model_result,
    MULTIPLE_ALIGNMENT_TASK: MultipleAlignment_result,
    PROBABILISTIC_NETWORKS_PROPS_TASK: ProbabilisticNetworksProperties_result,
    HYPER_GRAPHLETS_PROPS_TASK: HyperGraphletsProperties_result,
    SIMPLETS_PROPERTIES_TASK: SimpletsProperties_result,
    PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK: ProbabilisticNetworksNetAnalysis_result,
    PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK: ProbabilisticNetworksModelAnalysis_result,
    SIMPLETS_PAIRWISE_ANALYSIS_TASK: SimpletsPairwiseAnalysis_result,
    SIMPLETS_DVM_ANALYSIS_TASK: SimpletsDataVsModel_result,
    HYPERGRAPHLETS_NET_ANALYSIS_TASK: HyperGraphletsNetAnalysis_result,
    GraphletEigencentralities_TASK: GraphletEigencentralities_result,
    GraphletLaplacians_TASK: GraphletLaplacians_result,
    VISUALIZESE_TASK: VisualizeSE_result,
    # flag:NewTaskTemplate
    NEWTASKTEMPLATE_TASK: getrawdata_newtasktemplate,
}

DELETE_TASK_FUNCTION_MAPPINGS = {
    PAIRWISE_ANALYSIS_TASK: pairwise_analysis_delete,
    NETWORK_PROPERTIES_TASK: network_properties_delete,
    ALIGNMENT_TASK: alignment_delete,
    DATA_VS_MODEL_TASK: data_vs_model_delete,
    CANONICAL_CORRELATION_TASK: delete_canonical_task,
    DATA_FUSION_TASK: data_fusion_delete,
    DIRECTED_NETWORK_PROPERTIES_TASK: dn_network_properties_delete,
    DIRECTED_NETWORK_PAIRWISE_TASK: dn_pairwise_analysis_delete,
    DIRECTED_NETWORK_DVM_TASK: dn_data_vs_model_delete,
    MULTIPLE_ALIGNMENT_TASK: MultipleAlignment_delete,
    PROBABILISTIC_NETWORKS_PROPS_TASK: ProbabilisticNetworksProperties_delete,
    HYPER_GRAPHLETS_PROPS_TASK: HyperGraphletsProperties_delete,
    SIMPLETS_PROPERTIES_TASK: SimpletsProperties_delete,
    PROBABILISTIC_NETWORKS_NET_ANALYSIS_TASK: ProbabilisticNetworksNetAnalysis_delete,
    PROBABILISTIC_NETWORKS_MODEL_ANALYSIS_TASK: ProbabilisticNetworksModelAnalysis_delete,
    SIMPLETS_PAIRWISE_ANALYSIS_TASK: SimpletsPairwiseAnalysis_delete,
    SIMPLETS_DVM_ANALYSIS_TASK: SimpletsDataVsModel_delete,
    HYPERGRAPHLETS_NET_ANALYSIS_TASK: HyperGraphletsNetAnalysis_delete,
    GraphletEigencentralities_TASK: GraphletEigencentralities_delete,
    GraphletLaplacians_TASK: GraphletLaplacians_delete,
    VISUALIZESE_TASK: VisualizeSE_delete,
    # flag:NewTaskTemplate
    NEWTASKTEMPLATE_TASK: deletedata_newtasktemplate,
}

# NOTE:// If following status are changed, they need to be changed in dashboard/result.html as well
TASK_ERROR_STATUS = "Error"
TASK_RUNNING_STATUS = "Running"
TASK_FINISHED_STATUS = "Finished"