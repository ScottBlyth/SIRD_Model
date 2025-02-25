package com.example.sir;

import javafx.fxml.FXML;

import javafx.scene.control.TextField;

import java.util.Arrays;
import java.util.List;

public class ParameterBox {

    @FXML
    public TextField susceptible;
    @FXML
    public TextField infected;
    @FXML
    public TextField recovered;
    @FXML
    public TextField dead;

    @FXML
    public void initialize(){
        List<TextField> fields = Arrays.asList(susceptible, infected, recovered, dead);
        fields.forEach(x -> x.textProperty().addListener((obs, old, new_text) -> {
            if(!new_text.matches("$|\\d+$")) {
                x.setText(old);
            }
        }));
    }

}
