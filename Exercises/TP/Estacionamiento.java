package Exercises.TP;

public class Estacionamiento {
    private static final int NUM_ZONAS = 5;
    private static final int CAPACIDAD_ZONA = 7;
    // Cada zona es representada como un arreglo de Auto
    private Auto[][] zonas;

    public Estacionamiento() {
        zonas = new Auto[NUM_ZONAS][CAPACIDAD_ZONA];
    }

    // Clase interna que representa un Auto
    static class Auto {
        private String placa;
        private String marca;
        private String modelo;
        private String propietario;

        public Auto(String placa, String marca, String modelo, String propietario) {
            this.placa = placa;
            this.marca = marca;
            this.modelo = modelo;
            this.propietario = propietario;
        }

        public String getPlaca() {
            return placa;
        }

        @Override
        public String toString() {
            return "Auto{" +
                    "placa='" + placa + '\'' +
                    ", marca='" + marca + '\'' +
                    ", modelo='" + modelo + '\'' +
                    ", propietario='" + propietario + '\'' +
                    '}';
        }
    }

    /**
     * Parquea el auto en la primera posición disponible dentro de la zona indicada.
     * 
     * @param auto Auto a estacionar.
     * @param zona Zona en la que se desea estacionar (1 a 5).
     * @return true si se estacionó correctamente, false si la zona está llena o es
     *         inválida.
     */
    public boolean parquear(Auto auto, int zona) {
        if (zona < 1 || zona > NUM_ZONAS) {
            System.out.println("Zona inválida. Debe estar entre 1 y " + NUM_ZONAS);
            return false;
        }
        int indiceZona = zona - 1;
        for (int i = 0; i < CAPACIDAD_ZONA; i++) {
            if (zonas[indiceZona][i] == null) {
                zonas[indiceZona][i] = auto;
                System.out.println("Auto estacionado en zona " + zona + ", espacio " + (i + 1));
                return true;
            }
        }
        System.out.println("No hay espacio disponible en la zona " + zona);
        return false;
    }

    /**
     * Retira un auto de la zona indicada, buscando por su placa.
     * 
     * @param placa Placa del auto a retirar.
     * @param zona  Zona de la que se desea retirar el auto (1 a 5).
     * @return true si se retiró el auto, false si no se encontró.
     */
    public boolean retirar(String placa, int zona) {
        if (zona < 1 || zona > NUM_ZONAS) {
            System.out.println("Zona inválida. Debe estar entre 1 y " + NUM_ZONAS);
            return false;
        }
        int indiceZona = zona - 1;
        for (int i = 0; i < CAPACIDAD_ZONA; i++) {
            if (zonas[indiceZona][i] != null && zonas[indiceZona][i].getPlaca().equalsIgnoreCase(placa)) {
                zonas[indiceZona][i] = null;
                System.out.println("Auto con placa " + placa + " retirado de zona " + zona + ", espacio " + (i + 1));
                return true;
            }
        }
        System.out.println("Auto con placa " + placa + " no encontrado en la zona " + zona);
        return false;
    }

    /**
     * Muestra las ubicaciones de la zona indicada, listando cada espacio y su
     * estado.
     * 
     * @param zona Zona que se desea visualizar (1 a 5).
     */
    public void mostrarUbicaciones(int zona) {
        if (zona < 1 || zona > NUM_ZONAS) {
            System.out.println("Zona inválida. Debe estar entre 1 y " + NUM_ZONAS);
            return;
        }
        int indiceZona = zona - 1;
        System.out.println("Ubicaciones de la zona " + zona + ":");
        for (int i = 0; i < CAPACIDAD_ZONA; i++) {
            System.out.print("Espacio " + (i + 1) + ": ");
            if (zonas[indiceZona][i] == null) {
                System.out.println("Libre");
            } else {
                System.out.println(zonas[indiceZona][i]);
            }
        }
    }

    // Método main para demostrar el funcionamiento del estacionamiento
    public static void main(String[] args) {
        Estacionamiento estacionamiento = new Estacionamiento();

        // Crear algunos autos
        Auto auto1 = new Auto("ABC123", "Toyota", "Corolla", "Juan Perez");
        Auto auto2 = new Auto("DEF456", "Honda", "Civic", "Maria Lopez");
        Auto auto3 = new Auto("GHI789", "Ford", "Fiesta", "Carlos Ramirez");

        // Parquear autos en distintas zonas
        estacionamiento.parquear(auto1, 1);
        estacionamiento.parquear(auto2, 1);
        estacionamiento.parquear(auto3, 2);

        // Mostrar ubicaciones de la zona 1 y 2
        estacionamiento.mostrarUbicaciones(1);
        estacionamiento.mostrarUbicaciones(2);

        // Retirar un auto de la zona 1
        estacionamiento.retirar("DEF456", 1);
        estacionamiento.mostrarUbicaciones(1);
    }
}
