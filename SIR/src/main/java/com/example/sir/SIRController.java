package com.example.sir;

import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;

public class SIRController {

    @FXML
    private LineChart<Number, Number> epiChart;

    @FXML
    public void initialize() {
        XYChart.Series<Number, Number> series = new XYChart.Series<>();
        series.getData().add(new XYChart.Data<>(1,2));
        series.getData().add(new XYChart.Data<>(2,3));
        epiChart.getData().add(series);

    }

}