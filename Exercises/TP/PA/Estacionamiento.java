package Exercises.TP.PA;

class Auto {
    private String placa;
    private String marca;
    
    public Auto(String placa, String marca) {
        this.placa = placa;
        this.marca = marca;
    }
    
    public String toString() {
        return "Auto: " + placa + " (" + marca + ")";
    }
}

public class Estacionamiento {
    private Auto[][] zonas;
    private static final int NUM_ZONAS = 5;
    private static final int CAPACIDAD = 7;
    
    public Estacionamiento() {
        zonas = new Auto[NUM_ZONAS][CAPACIDAD];
    }
    
    // Procedimiento que parquea el auto en la primera ubicación disponible de la zona
    public boolean parquear(int zona, Auto auto) {
        if(zona < 0 || zona >= NUM_ZONAS) {
            System.out.println("Zona inválida.");
            return false;
        }
        for (int i = 0; i < CAPACIDAD; i++) {
            if(zonas[zona][i] == null) {
                zonas[zona][i] = auto;
                return true;
            }
        }
        System.out.println("Zona " + zona + " llena.");
        return false;
    }
    
    // Procedimiento que muestra el contenido de una zona
    public void mostrarZona(int zona) {
        if(zona < 0 || zona >= NUM_ZONAS) {
            System.out.println("Zona inválida.");
            return;
        }
        System.out.println("Contenido de la zona " + zona + ":");
        for (int i = 0; i < CAPACIDAD; i++) {
            System.out.println("Lugar " + i + ": " + (zonas[zona][i] != null ? zonas[zona][i] : "Vacío"));
        }
    }
    
    public static void main(String[] args) {
        Estacionamiento est = new Estacionamiento();
        Auto a1 = new Auto("ABC123", "Toyota");
        Auto a2 = new Auto("XYZ789", "Honda");
        est.parquear(1, a1);
        est.parquear(1, a2);
        est.mostrarZona(1);
    }
}
