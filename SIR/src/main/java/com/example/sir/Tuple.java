package com.example.sir;

public record Tuple<T, V>(T v1, V v2) {

    @Override
    public String toString() {
        return "["+v1+","+v2+"]";
    }
}
