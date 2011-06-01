function plotHierarchy() {
var root = pv.dom(hierarchy)
    .root("Hierarchy")

var vis = new pv.Panel()
    .width(400)
    .height(function() (root.nodes().length + 1) * 12)
    .margin(5);

var layout = vis.add(pv.Layout.Indent)
    .nodes(function() root.nodes())
    .depth(12)
    .breadth(12);

layout.link.add(pv.Line);

var node = layout.node.add(pv.Panel)
    .top(function(n) n.y - 6)
    .height(12)
    .right(6)
    .strokeStyle(null)
    .events("all")
    .event("mousedown", toggle);

node.anchor("left").add(pv.Dot)

    .strokeStyle(function(n) n.firstChild ? "#2eaadc" : "#a5a5a5")
    .fillStyle(function(n) n.toggled ? "#2eaadc" : n.firstChild ? "#ffffff" : "#a5a5a5")
    .title(function t(d) d.parentNode ? (t(d.parentNode) + "." + d.nodeName) : d.nodeName)
    .anchor("right").add(pv.Label)
    .text(function(n) n.nodeName);


vis.render();

/* Toggles the selected node, then updates the layout. */
function toggle(n) {
  n.toggle(pv.event.altKey);
  return layout.reset().root;
}

}
