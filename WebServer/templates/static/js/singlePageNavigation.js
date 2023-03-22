/**
 * Created by varun on 24/02/15.
 * Updated by carlos on 2022-jul
 */

var currentPageUrl = "";
var urlMappings = {};

function setUpUrlMappings() {
  var DASHBOARD = "dashboard";
  var NETWORK_PROPERTIES = "networkProperties";
  var ALIGNMENT = "alignment";
  var VISUALISE = "Visualise";
  var PAIRWISE_ANALYSIS = "pairwiseAnalysis";
  var DATA_VS_MODEL = "DataVsModel";
  var ADMIN_CENTER = "AdminCenter";
  var CANONICAL_ANALYSIS = "Canonical";
  var DataFusion = "DataFusion";
  var DirectedNetworkProperties = "DirectedNetworkProperties";
  var DirectedNetworkPairwise = "DirectedNetworkPairwise";
  var DirectedNetworkDataVsModel = "DirectedNetworkDataVsModel";
  var MultipleAlignment = "MultipleAlignment";
  var ProbabilisticNetworksProperties = "ProbabilisticNetworksProperties";
  var HyperGraphletsProperties = "HyperGraphletsProperties";
  var SimpletsProperties = "SimpletsProperties";
  var ProbabilisticNetworksNetAnalysis = "ProbabilisticNetworksNetAnalysis";
  var ProbabilisticNetworksModelAnalysis = "ProbabilisticNetworksModelAnalysis";
  var SimpletsPairwiseAnalysis = "SimpletsPairwiseAnalysis";
  var SimpletsDataVsModel = "SimpletsDataVsModel";
  var HyperGraphletsNetAnalysis = "HyperGraphletsNetAnalysis";
  var ClusteringAndEnrichment = "ClusteringAndEnrichment";
  // var  = "";
  // flag:NewTaskTemplate
  var NewTaskTemplate = "NewTaskTemplate";

  // urlMappings["/" + DASHBOARD + "/"] = DASHBOARD;
  urlMappings["/" + DASHBOARD + "/gc/"] = DASHBOARD;
  urlMappings["/" + NETWORK_PROPERTIES + "/"] = NETWORK_PROPERTIES;
  urlMappings["/" + ALIGNMENT + "/"] = ALIGNMENT;
  urlMappings["/" + VISUALISE + "/"] = VISUALISE;
  urlMappings["/" + PAIRWISE_ANALYSIS + "/"] = PAIRWISE_ANALYSIS;
  urlMappings["/" + DATA_VS_MODEL + "/"] = DATA_VS_MODEL;
  urlMappings["/" + ADMIN_CENTER + "/"] = ADMIN_CENTER;
  urlMappings["/" + CANONICAL_ANALYSIS + "/"] = CANONICAL_ANALYSIS;
  urlMappings["/" + DataFusion + "/"] = DataFusion;
  urlMappings["/" + DirectedNetworkProperties + "/"] = DirectedNetworkProperties;
  urlMappings["/" + DirectedNetworkPairwise + "/"] = DirectedNetworkPairwise;
  urlMappings["/" + DirectedNetworkDataVsModel + "/"] = DirectedNetworkDataVsModel;
  urlMappings["/" + MultipleAlignment + "/"] = MultipleAlignment;
  urlMappings["/" + ProbabilisticNetworksProperties + "/"] = ProbabilisticNetworksProperties;
  urlMappings["/" + HyperGraphletsProperties + "/"] = HyperGraphletsProperties;
  urlMappings["/" + SimpletsProperties + "/"] = SimpletsProperties;
  urlMappings["/" + ProbabilisticNetworksNetAnalysis + "/"] = ProbabilisticNetworksNetAnalysis;
  urlMappings["/" + ProbabilisticNetworksModelAnalysis + "/"] = ProbabilisticNetworksModelAnalysis;
  urlMappings["/" + SimpletsPairwiseAnalysis + "/"] = SimpletsPairwiseAnalysis;
  urlMappings["/" + SimpletsPairwiseAnalysis + "/page_dvm/"] = SimpletsDataVsModel;
  urlMappings["/" + HyperGraphletsNetAnalysis + "/"] = HyperGraphletsNetAnalysis;
  urlMappings["/" + ClusteringAndEnrichment + "/clustering_and_enrichment_analysis/"] = ClusteringAndEnrichment;
  // urlMappings["/" +  + "/"] = ;
  // flag:NewTaskTemplate
  urlMappings["/" + NewTaskTemplate + "/"] = NewTaskTemplate;
}

function navigateTo(url) {
  Pace.track(function () {
    $.ajax({
      url: url,
      type: 'GET',
      success: function (data) {
        $("#mainContent").html(data);
        // console.log('navigateTo url: ' + url);
        setCurrentUrlMenuItemToActive(url);
        currentPageUrl = url;
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log('ERRORS: ' + textStatus);
      }
    });
  })
}

function setCurrentUrlMenuItemToActive(url) {
  // console.log('currentPageUrl: ' + currentPageUrl);
  // console.log('going to: ' + url);
  if (currentPageUrl in urlMappings) {
    $("#" + urlMappings[currentPageUrl]).removeClass("active");
  }
  if (url in urlMappings) {
    // console.log('adding active to: ' + urlMappings[url]);
    $("#" + urlMappings[url]).addClass("active");
  }
}
setUpUrlMappings();