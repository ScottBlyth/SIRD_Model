package com.example.sir;


import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;
import javafx.scene.shape.Line;

import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

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
    private List<Circle> circles = new ArrayList<>();

    @FXML
    public void initialize() {
        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.getData().add(new XYChart.Data<>(1,2));
        series.getData().add(new XYChart.Data<>(2,3));
        series.setName("Infections");
        epiChart.getData().add(series);
    }

    @FXML
    public void clickOnGraph(MouseEvent mouseEvent) {
        if(createNodeOnClick) {
            Circle circle = new Circle(mouseEvent.getX(), mouseEvent.getY(), 10);
            graph.addNode();
            int circleID = graph.numNodes()-1;
            circle.setId("C"+circleID);
            circle.setOnMouseClicked(mouseEvent1 -> {
                if(selectedNode){
                    if(vertexSelected == circleID) {
                        resetSelection();
                    }else {
                        graph.addEdge(vertexSelected, circleID, 0.01f);
                        graph.addEdge(circleID, vertexSelected, 0.01f);
                        Line line = createLine(nodeSelected.getCenterX(), nodeSelected.getCenterY(),
                        circle.getCenterX(), circle.getCenterY(), circle.getRadius());
                        cityGraph.getChildren().add(line);
                        // deselect everything
                        resetSelection();
                    }
                }else {
                    selectedNode = true;
                    vertexSelected = circleID;
                    nodeSelected = circle;
                    circle.setFill(Paint.valueOf("black"));
                }

            });
            circles.add(circle);
            cityGraph.getChildren().add(circle);
            circle.getStyleClass().add("node");
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
        List<Tuple<Double, Double>> positions = new ArrayList<>();
        for(Circle circle : circles) {
            positions.add(new Tuple<>(circle.getCenterX(), circle.getCenterY()));
        }
        FileWriter writer = new FileWriter("map.json");
        writer.write(graph.toJson(positions).toJSONString());
        writer.close();
    }

    @FXML
    public void load() {
        JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter("json files","json");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(null);
        if(returnVal == JFileChooser.APPROVE_OPTION) {
            System.out.println(chooser.getSelectedFile().getName());
        }
    }

    private void resetSelection() {
        selectedNode = false;
        vertexSelected=-1;
        nodeSelected.setFill(Paint.valueOf("rgba(0,0,0,0)"));
        nodeSelected = null;
    }

    private Line createLine(double sx, double sy, double ex, double ey, double r) {
        Line line = new Line();
        double diffX = ex-sx;
        double diffY = ey-sy;
        double size = Math.sqrt(diffX*diffX+diffY*diffY);
        diffX /= size;
        diffY /= size;
        sx = sx + r * diffX;
        sy = sy + r * diffY;
        ex = ex - r*diffX;
        ey = ey - r*diffY;
        line.setStartX(sx);
        line.setStartY(sy);
        line.setEndX(ex);
        line.setEndY(ey);
        line.setStrokeWidth(3);
        line.setFill(Paint.valueOf("red"));
        line.setStroke(Paint.valueOf("red"));
        return line;
    }

}