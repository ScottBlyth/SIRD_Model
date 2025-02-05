module com.example.sir {
    requires javafx.controls;
    requires javafx.fxml;
    requires json.simple;
    requires java.desktop;


    opens com.example.sir to javafx.fxml;
    exports com.example.sir;
    exports com.example.sir.server;
    opens com.example.sir.server to javafx.fxml;
}