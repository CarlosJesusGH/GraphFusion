from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from authentication import urls as authentication_urls
from dashboard import urls as dashboard_urls
from NetworkProperties import urls as network_props_urls
from NetworkAlignment import urls as network_align_urls
from PairwiseAnalysis import urls as pairwise_analysis_urls
from Visualise import urls as visualise_urls
from UserProfile import urls as profile_urls
from TaskFactory import urls as task_urls
from DataVsModelAnalysis import urls as data_vs_model_urls
from AdminCenter import urls as admin_center_urls
from CanonicalCorrelationAnalysis import urls as canonical_urls
from DataFusion import urls as data_fusion_urls
from DirectedNetworkProperties import urls as dn_properties_urls
from DirectedNetworkPairwise import urls as dn_pairwise_urls
from DirectedNetworkDataVsModel import urls as dn_dvm_urls
from MultipleAlignment import urls as MultipleAlignment_align_urls
from ProbabilisticNetworksProperties import urls as ProbabilisticNetworksProperties_urls
from HyperGraphletsProperties import urls as HyperGraphletsProperties_urls
from SimpletsProperties import urls as SimpletsProperties_urls
from ProbabilisticNetworksNetAnalysis import urls as ProbabilisticNetworksNetAnalysis_urls
from ProbabilisticNetworksModelAnalysis import urls as ProbabilisticNetworksModelAnalysis_urls
from SimpletsPairwiseAnalysis import urls as SimpletsPairwiseAnalysis_urls
from HyperGraphletsNetAnalysis import urls as HyperGraphletsNetAnalysis_urls
from ClusteringAndEnrichment import urls as ClusteringAndEnrichment_urls
from TopologicalAnalysis import urls as TopologicalAnalysis_urls
from GraphletEigencentralities import urls as GraphletEigencentralities_urls
from GraphletLaplacians import urls as GraphletLaplacians_urls
# flag:NewTaskTemplate
from a_NewTaskTemplate import urls as newtasktemplate_urls

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^media/(?P<path>.*)/$', 'django.views.static.serve', {'document_root': MEDIA_URL, 'show_indexes': False}),
    url(r'^networkProperties/', include(network_props_urls.urlpatterns)),
    url(r'^alignment/', include(network_align_urls.urlpatterns)),
    url(r'^pairwiseAnalysis/', include(pairwise_analysis_urls.urlpatterns)),
    url(r'^Visualise/', include(visualise_urls.urlpatterns)),
    url(r'^Profile/', include(profile_urls.urlpatterns)),
    url(r'^TaskFactory/', include(task_urls.urlpatterns)),
    url(r'^DataVsModel/', include(data_vs_model_urls.urlpatterns)),
    url(r'^AdminCenter/', include(admin_center_urls.urlpatterns)),
    url(r'^Canonical/', include(canonical_urls.urlpatterns)),
    url(r'^dashboard/', include(dashboard_urls.urlpatterns)),
    url(r'^', include(authentication_urls.urlpatterns)),
    url(r'^$', RedirectView.as_view(url='/')),
    url(r'^DataFusion/', include(data_fusion_urls.urlpatterns)),
    url(r'^DirectedNetworkProperties/', include(dn_properties_urls.urlpatterns)),
    url(r'^DirectedNetworkPairwise/', include(dn_pairwise_urls.urlpatterns)),
    url(r'^DirectedNetworkDataVsModel/', include(dn_dvm_urls.urlpatterns)),
    url(r'^MultipleAlignment/', include(MultipleAlignment_align_urls.urlpatterns)),
    url(r'^ProbabilisticNetworksProperties/', include(ProbabilisticNetworksProperties_urls.urlpatterns)),
    url(r'^HyperGraphletsProperties/', include(HyperGraphletsProperties_urls.urlpatterns)),
    url(r'^SimpletsProperties/', include(SimpletsProperties_urls.urlpatterns)),
    url(r'^ProbabilisticNetworksNetAnalysis/', include(ProbabilisticNetworksNetAnalysis_urls.urlpatterns)),
    url(r'^ProbabilisticNetworksModelAnalysis/', include(ProbabilisticNetworksModelAnalysis_urls.urlpatterns)),
    url(r'^SimpletsPairwiseAnalysis/', include(SimpletsPairwiseAnalysis_urls.urlpatterns)),
    url(r'^HyperGraphletsNetAnalysis/', include(HyperGraphletsNetAnalysis_urls.urlpatterns)),
    url(r'^ClusteringAndEnrichment/', include(ClusteringAndEnrichment_urls.urlpatterns)),
    url(r'^TopologicalAnalysis/', include(TopologicalAnalysis_urls.urlpatterns)),
    url(r'^GraphletEigencentralities/', include(GraphletEigencentralities_urls.urlpatterns)),
    url(r'^GraphletLaplacians/', include(GraphletLaplacians_urls.urlpatterns)),
    # url(r'^/', include(_urls.urlpatterns)),
    # flag:NewTaskTemplate
    url(r'^NewTaskTemplate/', include(newtasktemplate_urls.urlpatterns)),
)
