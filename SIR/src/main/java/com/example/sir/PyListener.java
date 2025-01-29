package com.example.sir;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class PyListener {

    private ServerSocket socket;

    public PyListener(int port) throws IOException {
        socket = new ServerSocket(port);
    }

    

}
