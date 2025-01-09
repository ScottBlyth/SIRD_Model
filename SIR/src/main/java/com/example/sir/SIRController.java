package com.example.sir;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.input.MouseEvent;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Paint;
import javafx.scene.shape.Circle;

public class SIRController {
    @FXML
    private LineChart<Number, Number> epiChart;
    @FXML
    private Pane cityGraph;
    private boolean createNodeOnClick = false;

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
            Circle circle = new Circle(mouseEvent.getX(), mouseEvent.getY(), 10, Paint.valueOf("blue"));
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

}