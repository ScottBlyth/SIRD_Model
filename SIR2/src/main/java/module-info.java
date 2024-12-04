module com.example.sir {
    requires javafx.controls;
    requires javafx.fxml;


    opens com.example.sir to javafx.fxml;
    exports com.example.sir;
}