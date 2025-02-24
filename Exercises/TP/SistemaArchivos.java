package Exercises.TP;

import java.util.ArrayList;
import java.util.Date;

// Clase base para Carpeta y Archivo
abstract class Elemento {
    protected String nombre;
    protected Date fechaCreacion;

    public Elemento(String nombre) {
        this.nombre = nombre;
        this.fechaCreacion = new Date(); // Fecha y hora actual
    }

    public String getNombre() {
        return nombre;
    }

    public Date getFechaCreacion() {
        return fechaCreacion;
    }
}

// Clase Archivo: tiene nombre, fecha de creación y tamaño en bytes
class Archivo extends Elemento {
    private long tamañoBytes;

    public Archivo(String nombre, long tamañoBytes) {
        super(nombre);
        this.tamañoBytes = tamañoBytes;
    }

    public long getTamañoBytes() {
        return tamañoBytes;
    }

    @Override
    public String toString() {
        return "Archivo{" +
                "nombre='" + nombre + '\'' +
                ", fechaCreacion=" + fechaCreacion +
                ", tamañoBytes=" + tamañoBytes +
                '}';
    }
}

// Clase Carpeta: tiene nombre, fecha de creación, referencia a la carpeta padre
// y
// una lista de elementos (carpetas o archivos) con un máximo de 5 elementos.
class Carpeta extends Elemento {
    private Carpeta padre;
    private ArrayList<Elemento> elementos;
    public static final int MAX_ELEMENTOS = 5;

    public Carpeta(String nombre, Carpeta padre) {
        super(nombre);
        this.padre = padre;
        this.elementos = new ArrayList<>();
    }

    public Carpeta getPadre() {
        return padre;
    }

    // Agrega un elemento si aún no se alcanzó el máximo
    public boolean agregarElemento(Elemento e) {
        if (elementos.size() < MAX_ELEMENTOS) {
            elementos.add(e);
            return true;
        }
        return false;
    }

    // Busca un elemento (carpeta o archivo) por nombre
    public Elemento buscarElemento(String nombre) {
        for (Elemento e : elementos) {
            if (e.getNombre().equalsIgnoreCase(nombre)) {
                return e;
            }
        }
        return null;
    }

    public ArrayList<Elemento> getElementos() {
        return elementos;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("Carpeta{")
                .append("nombre='").append(nombre).append('\'')
                .append(", fechaCreacion=").append(fechaCreacion)
                .append(", elementos=").append(elementos)
                .append('}');
        return sb.toString();
    }
}

// Clase SistemaArchivos: administra el sistema de carpetas y archivos.
// Permite crear carpetas/archivos, entrar a una carpeta, subir de nivel y ver
// la ruta actual.
public class SistemaArchivos {
    private Carpeta root;
    private Carpeta carpetaActual;

    public SistemaArchivos() {
        // La carpeta raíz no tiene padre
        root = new Carpeta("root", null);
        carpetaActual = root;
    }

    // Entra a una carpeta dentro de la carpeta actual, según el nombre
    public boolean entrar(String nombre) {
        Elemento e = carpetaActual.buscarElemento(nombre);
        if (e != null && e instanceof Carpeta) {
            carpetaActual = (Carpeta) e;
            System.out.println("Entrando a la carpeta: " + nombre);
            return true;
        } else {
            System.out.println("Carpeta no encontrada: " + nombre);
            return false;
        }
    }

    // Sube un nivel (vuelve a la carpeta padre)
    public void subir() {
        if (carpetaActual.getPadre() != null) {
            System.out.println("Subiendo a la carpeta: " + carpetaActual.getPadre().getNombre());
            carpetaActual = carpetaActual.getPadre();
        } else {
            System.out.println("Ya se encuentra en la carpeta raíz.");
        }
    }

    // Muestra la ruta actual desde la raíz
    public void verRuta() {
        System.out.println("Ruta actual: " + obtenerRuta(carpetaActual));
    }

    private String obtenerRuta(Carpeta carpeta) {
        if (carpeta.getPadre() == null)
            return "/" + carpeta.getNombre();
        else
            return obtenerRuta(carpeta.getPadre()) + "/" + carpeta.getNombre();
    }

    // Crea una nueva carpeta en la carpeta actual
    public void crearCarpeta(String nombre) {
        Carpeta nueva = new Carpeta(nombre, carpetaActual);
        if (carpetaActual.agregarElemento(nueva)) {
            System.out.println("Carpeta creada: " + nombre);
        } else {
            System.out.println("No se pudo crear la carpeta. Máximo de elementos alcanzado.");
        }
    }

    // Crea un nuevo archivo en la carpeta actual
    public void crearArchivo(String nombre, long tamañoBytes) {
        Archivo archivo = new Archivo(nombre, tamañoBytes);
        if (carpetaActual.agregarElemento(archivo)) {
            System.out.println("Archivo creado: " + nombre);
        } else {
            System.out.println("No se pudo crear el archivo. Máximo de elementos alcanzado.");
        }
    }

    // Método main para demostrar el funcionamiento del sistema de archivos
    public static void main(String[] args) {
        SistemaArchivos sistema = new SistemaArchivos();
        sistema.verRuta(); // Muestra /root

        // Crear carpetas y archivos en la raíz
        sistema.crearCarpeta("Documentos");
        sistema.crearArchivo("nota.txt", 1024);

        // Entrar a la carpeta Documentos
        sistema.entrar("Documentos");
        sistema.verRuta(); // Muestra /root/Documentos

        // Crear elementos dentro de Documentos
        sistema.crearArchivo("informe.doc", 2048);
        sistema.crearCarpeta("Fotos");

        // Entrar a la carpeta Fotos
        sistema.entrar("Fotos");
        sistema.verRuta(); // Muestra /root/Documentos/Fotos

        // Subir un nivel
        sistema.subir();
        sistema.verRuta(); // Muestra /root/Documentos

        // Intentar subir desde la raíz
        sistema.subir();
        sistema.verRuta(); // Muestra /root
    }
}
