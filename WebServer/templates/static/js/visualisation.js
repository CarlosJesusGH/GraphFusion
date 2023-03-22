/**
 * Created by varun on 01/05/15.
 */


function drawGraph(container, graphNodes, graphEdges, network) {
  var nodes = graphNodes;
  var edges = graphEdges;

  // create a network
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {
    physics: {barnesHut: {springLength: 150}}, // this is the correct way to set the length of the springs
    clustering: {
      enabled: false
    },
    stabilize: true
  };
  network = new vis.Network(container, data, options);

  // add event listeners
  network.on('select', function (params) {
    document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });
}
