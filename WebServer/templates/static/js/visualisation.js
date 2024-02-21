/**
 * Created by varun on 01/05/15.
 */


function drawGraph(container, graphNodes, graphEdges, network, directed=false) {
  console.log("visualisation.js - drawGraph - start");
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
  var options_old = {
    // physics: {barnesHut: {springLength: 150}}, // this is the correct way to set the length of the springs
    // make:
    // "physics": {
      //   "enabled": false,
      //   "minVelocity": 0.75
      // }
    // physics: {
    //   enabled: false,
    //   minVelocity: 0.75,
    //   // stabilization: false,
    // },
    // physics:{
    //   enabled:true
    // },
    physics: {
      stabilization: {
          enabled: true,
          iterations: 50, // maximum number of iteration to stabilize
          updateInterval: 10,
          onlyDynamicEdges: false,
          fit: true
      },
    },
    // clustering: {
    //   enabled: false
    // },
    // stabilize: true,
    // from: https://stackoverflow.com/questions/56586628/how-to-force-edge-direction-using-vis-js
    edges: {
      arrows: {
        to: {
          enabled: directed,
          scaleFactor: 0.5,
          type: "arrow"
        }
      },
      nodes: {
        shapeProperties: {
          interpolation: false    // 'true' for intensive zooming
        }
      },
      // smooth: {
      //   type: 'continuous'
      // }
    },
  };

  var options = {
    autoResize: true,
    height: '400px',
    clickToUse: false,
    layout: {
      hierarchical: {
        direction: 'UD',
        sortMethod: 'directed',
      }
    },
    nodes: {
      shape: 'dot',
      size: 20,
      font: {
        size: 15,
        color: '#ffffff'
      },
      borderWidth: 2
    }
  };

  // From vis.js https://github.com/almende/vis
  // nice network example: https://visjs.github.io/vis-network/examples/network/edgeStyles/smoothWorldCup.html
  network = new vis.Network(container, data, options);

  // add event listeners
  network.on('select', function (params) {
    // document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
    console.log("event listener - select - " + params.nodes);
  });

  // TODO: add a listener for when the graph is stabilised
  network.on('stabilized', function (params) {
    console.log("event listener - stabilized - " + params.nodes);
    // document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });

  // TODO: add a listener for when the graph is ready. Also remove the loading spinner
  network.on('ready', function (params) {
    console.log("event listener - ready - " + params.nodes);
    // document.getElementById('selection').innerHTML = 'Selection: ' + params.nodes;
  });



  console.log("visualisation.js - drawGraph - end");
}
