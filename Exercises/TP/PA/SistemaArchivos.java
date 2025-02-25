package Exercises.TP.PA;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

class Archivo {
    private String nombre;
    private long tamano; // en bytes
    private LocalDateTime fechaCreacion;

    public Archivo(String nombre, long tamano) {
        this.nombre = nombre;
        this.tamano = tamano;
        this.fechaCreacion = LocalDateTime.now();
    }

    // Función que retorna la información del archivo
    public String toString() {
        return "Archivo: " + nombre + " (" + tamano + " bytes, creado: " + fechaCreacion + ")";
    }
}

class Carpeta {
    private String nombre;
    private List<Object> elementos; // Puede contener archivos u otras carpetas
    private static final int MAX_ELEMENTOS = 5;

    public Carpeta(String nombre) {
        this.nombre = nombre;
        this.elementos = new ArrayList<>();
    }

    // Procedimiento que agrega un elemento a la carpeta
    public boolean agregarElemento(Object elem) {
        if (elementos.size() < MAX_ELEMENTOS) {
            elementos.add(elem);
            return true;
        }
        System.out.println("Carpeta llena: " + nombre);
        return false;
    }

    // Procedimiento que muestra el contenido de la carpeta
    public void listarElementos() {
        System.out.println("Contenido de la carpeta " + nombre + ":");
        for (Object e : elementos) {
            System.out.println(" - " + e);
        }
    }
}

public class SistemaArchivos {
    public static void main(String[] args) {
        Carpeta raiz = new Carpeta("root");
        Archivo arch1 = new Archivo("doc.txt", 1000);
        Archivo arch2 = new Archivo("foto.jpg", 5000);
        raiz.agregarElemento(arch1);
        raiz.agregarElemento(arch2);
        raiz.listarElementos();
    }
}
