import java.util.Scanner;

public class CalculadoraTarifasEnvio {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
    

        System.out.print("Ingrese el peso de paquete en kg: ");
        double peso = scanner.nextDouble();
  
        System.out.print("Seleccione el tipo de envío 1-Local 2-Nacional 3-Internacional ");
        int tipoEnvio = scanner.nextInt();
        
  
        System.out.print("El cliente es miembro premium S o N  ");
        char esPremium = scanner.next().charAt(0);
        
     
        double tarifa = 0;
        
        if (peso <= 1) {
            tarifa = 5;
        } else if (peso > 1 && peso <= 5) {
            tarifa = 10;
        } else if (peso > 5 && peso <= 10) {
            tarifa = 15;
        } else {
            tarifa = 25;
        }
        
      
        double distancia_ta = tarifa;
        
        if (tipoEnvio == 2) { 
            distancia_ta = tarifa * 1.20;
        } else if (tipoEnvio == 3) { 
            distancia_ta = tarifa * 1.50;
        }
       
        double final_f = distancia_ta;
        
        if (esPremium == 'S' || esPremium == 's') {
            final_f = distancia_ta * 0.85;
        }
  
        System.out.printf("El costo final de envío es: $%.2f", final_f);
        
        scanner.close();
    }
}