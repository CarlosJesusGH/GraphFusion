/**
 * Created by varun on 01/05/15.
 */


function drawGraph(container, graphNodes, graphEdges, network, directed=false) {
  var nodes = graphNodes;
  var edges = graphEdges;

  // Check if directed is true
  directed = directed == "True";
  // console.log("drawGraph directed: " + directed);

  // create a network
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    physics: {barnesHut: {springLength: 150}}, // this is the correct way to set the length of the springs
    // clustering: {
    //   enabled: false
    // },
    stabilize: true,
    // from: https://stackoverflow.com/questions/56586628/how-to-force-edge-direction-using-vis-js
    edges: {
      arrows: {
        to: {
          enabled: directed,
          scaleFactor: 0.5,
          type: "arrow"
        }
      },
      smooth: {
        type: 'continuous'
      }
    },
  };
  // From vis.js https://github.com/almende/vis
  // nice network example: https://visjs.github.io/vis-network/examples/network/edgeStyles/smoothWorldCup.html
  network = new vis.Network(container, data, options);

  // add event listeners
  network.on('select', function (params) {
    document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });
}
