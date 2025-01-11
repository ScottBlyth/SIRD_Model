package com.example.sir;


import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;

import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;

public class SIRController {
    @FXML
    private LineChart<Number, Number> epiChart;
    @FXML
    private Pane cityGraph;
    private boolean createNodeOnClick = false;

    private boolean selectedNode = false;
    private Integer vertexSelected = -1;
    private Circle nodeSelected;
    private final Graph graph = new Graph();

    @FXML
    public void initialize() {
        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.getData().add(new XYChart.Data<>(1,2));
        series.getData().add(new XYChart.Data<>(2,3));
        series.setName("Infections");
        epiChart.getData().add(series);

        GraphFactory factory = new GraphFactory();
        try {
            Graph test = factory.createGraph("map.json");
        }catch (Exception e) {

        }
    }

    @FXML
    public void clickOnGraph(MouseEvent mouseEvent) {
        if(createNodeOnClick) {
            Circle circle = new Circle(mouseEvent.getX(), mouseEvent.getY(), 10, Paint.valueOf("blue"));
            graph.addNode();
            int circleID = graph.numNodes()-1;
            circle.setOnMouseClicked(mouseEvent1 -> {
                if(selectedNode){
                    if(vertexSelected == circleID) {
                        resetSelection();
                    }else {
                        graph.addEdge(vertexSelected, circleID, 0.01f);
                        graph.addEdge(circleID, vertexSelected, 0.01f);
                        Line line = createLine(nodeSelected.getCenterX(), nodeSelected.getCenterY(),
                        circle.getCenterX(), circle.getCenterY());
                        cityGraph.getChildren().add(line);
                        // deselect everything
                        resetSelection();
                    }
                }else {
                    selectedNode = true;
                    vertexSelected = circleID;
                    nodeSelected = circle;
                    circle.setStroke(Paint.valueOf("black"));
                    circle.setStrokeWidth(2);
                }

            });
            cityGraph.getChildren().add(circle);
        }
    }

    @FXML
    public void toggleCreateNode() {
        createNodeOnClick = true;
    }

    @FXML
    public void toggleCreateLink() {
        createNodeOnClick = false;
    }

    @FXML
    public void save() throws IOException {
        FileWriter writer = new FileWriter("map.json");
        writer.write(graph.toJson());
        writer.close();
    }

    private void resetSelection() {
        selectedNode = false;
        vertexSelected=-1;
        nodeSelected.setStrokeWidth(0);
        nodeSelected = null;
    }

    private Line createLine(double sx, double sy, double ex, double ey) {
        Line line = new Line();
        line.setStartX(sx);
        line.setStartY(sy);
        line.setEndX(ex);
        line.setEndY(ey);
        line.setStrokeWidth(3);
        line.setFill(Paint.valueOf("black"));
        return line;
    }

}