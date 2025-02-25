package Exercises.TP.PA;

public class CalculadoraSimple {
    // Función que suma dos números
    public static int sumar(int a, int b) {
        return a + b;
    }
    
    // Función que resta dos números
    public static int restar(int a, int b) {
        return a - b;
    }
    
    // Función que multiplica dos números
    public static int multiplicar(int a, int b) {
        return a * b;
    }
    
    // Función que divide dos números
    public static double dividir(int a, int b) {
        if (b != 0) {
            return (double) a / b;
        } else {
            throw new IllegalArgumentException("División por cero no permitida.");
        }
    }
    
    public static void main(String[] args) {
        int a = 12, b = 4;
        System.out.println("Suma: " + sumar(a, b));
        System.out.println("Resta: " + restar(a, b));
        System.out.println("Multiplicación: " + multiplicar(a, b));
        System.out.println("División: " + dividir(a, b));
    }
}
