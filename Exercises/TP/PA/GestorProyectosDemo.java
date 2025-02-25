package Exercises.TP.PA;

class Proyecto {
    private int codigo;
    private String nombre;
    
    public Proyecto(int codigo, String nombre) {
        this.codigo = codigo;
        this.nombre = nombre;
    }
    
    public int getCodigo() {
        return codigo;
    }
    
    public String getNombre() {
        return nombre;
    }
    
    public String toString() {
        return "Proyecto " + codigo + ": " + nombre;
    }
}

class GestorProyectos {
    private Proyecto[] proyectos;
    private int contador;
    private static final int MAX = 10;
    
    public GestorProyectos() {
        proyectos = new Proyecto[MAX];
        contador = 0;
    }
    
    // Procedimiento para agregar un proyecto
    public void agregar(Proyecto p) {
        if (contador < MAX) {
            proyectos[contador++] = p;
        } else {
            System.out.println("Máximo de proyectos alcanzado.");
        }
    }
    
    // Función que busca un proyecto por código
    public Proyecto buscar(int codigo) {
        for (int i = 0; i < contador; i++) {
            if (proyectos[i].getCodigo() == codigo) {
                return proyectos[i];
            }
        }
        return null;
    }
    
    // Procedimiento que lista todos los proyectos
    public void listarProyectos() {
        System.out.println("Proyectos:");
        for (int i = 0; i < contador; i++) {
            System.out.println(proyectos[i]);
        }
    }
}

public class GestorProyectosDemo {
    public static void main(String[] args) {
        GestorProyectos gp = new GestorProyectos();
        gp.agregar(new Proyecto(101, "Proyecto A"));
        gp.agregar(new Proyecto(102, "Proyecto B"));
        gp.agregar(new Proyecto(103, "Proyecto C"));
        gp.listarProyectos();
        
        Proyecto buscado = gp.buscar(102);
        if (buscado != null) {
            System.out.println("Proyecto encontrado: " + buscado);
        } else {
            System.out.println("Proyecto no encontrado.");
        }
    }
}
