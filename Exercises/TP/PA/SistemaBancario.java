package Exercises.TP.PA;

class CuentaBancaria {
    private String titular;
    private double saldo;

    public CuentaBancaria(String titular, double saldoInicial) {
        this.titular = titular;
        this.saldo = saldoInicial;
    }

    // Procedimiento para depositar dinero
    public void depositar(double cantidad) {
        if (cantidad > 0) {
            saldo += cantidad;
        }
    }

    // Función que retira dinero y retorna verdadero si la operación es exitosa
    public boolean retirar(double cantidad) {
        if (cantidad > 0 && saldo >= cantidad) {
            saldo -= cantidad;
            return true;
        }
        return false;
    }

    public double getSaldo() {
        return saldo;
    }

    @Override
    public String toString() {
        return "Cuenta de " + titular + " - Saldo: " + saldo;
    }
}

public class SistemaBancario {
    public static void main(String[] args) {
        CuentaBancaria cuenta = new CuentaBancaria("Carlos", 1000);
        System.out.println("Inicial: " + cuenta);
        cuenta.depositar(500);
        System.out.println("Después de depositar 500: " + cuenta);
        boolean retirado = cuenta.retirar(300);
        System.out.println("Retiro de 300 " + (retirado ? "exitoso" : "fallido") + ": " + cuenta);
    }
}
