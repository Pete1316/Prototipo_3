import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CalculadoraGUI extends JFrame {
    private JTextField num1Field, num2Field, resultadoField;
    private Calculadora calculadora;

    public CalculadoraGUI() {
        calculadora = new Calculadora();
        
        setTitle("Calculadora Gráfica");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridLayout(5, 2, 10, 10));
        
        // Componentes de la interfaz
        add(new JLabel("Número 1:"));
        num1Field = new JTextField();
        add(num1Field);
        
        add(new JLabel("Número 2:"));
        num2Field = new JTextField();
        add(num2Field);
        
        add(new JLabel("Resultado:"));
        resultadoField = new JTextField();
        resultadoField.setEditable(false);
        add(resultadoField);
        
        // Botones de operaciones
        JButton sumaBtn = new JButton("Suma");
        sumaBtn.addActionListener(new OperacionListener(new Suma()));
        add(sumaBtn);
        
        JButton restaBtn = new JButton("Resta");
        restaBtn.addActionListener(new OperacionListener(new Resta()));
        add(restaBtn);
        
        JButton multiplicacionBtn = new JButton("Multiplicación");
        multiplicacionBtn.addActionListener(new OperacionListener(new Multiplicacion()));
        add(multiplicacionBtn);
        
        JButton divisionBtn = new JButton("División");
        divisionBtn.addActionListener(new OperacionListener(new Division()));
        add(divisionBtn);
        
        setVisible(true);
    }
    
    private class OperacionListener implements ActionListener {
        private Operacion operacion;
        
        public OperacionListener(Operacion operacion) {
            this.operacion = operacion;
        }
        
        @Override
        public void actionPerformed(ActionEvent e) {
            try {
                double num1 = Double.parseDouble(num1Field.getText());
                double num2 = Double.parseDouble(num2Field.getText());
                
                double resultado = calculadora.realizarOperacion(operacion, num1, num2);
                resultadoField.setText(String.valueOf(resultado));
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(CalculadoraGUI.this, 
                    "Por favor ingrese números válidos", "Error", JOptionPane.ERROR_MESSAGE);
            } catch (ArithmeticException ex) {
                JOptionPane.showMessageDialog(CalculadoraGUI.this, 
                    ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
            }
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CalculadoraGUI());
    }
}