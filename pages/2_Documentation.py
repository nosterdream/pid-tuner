import streamlit as st


st.write("# PID Tuner Documentation")

st.markdown("""
- [Introduction and PID Basics](#Introduction)
- [Object Models](#Object)
- [PID Basics](#PID_Basics)
    - [PID Forms](#Forms)
    - [Mathematical Description of Ideal Controllers](#Math_forms)
    - [PID in various DCS](#DCS)
- [Data Loading](#Loading)
- [Model Fitting](#Fitting)
- [PID Tuning](#Tuning)
- [References](#References)
""", unsafe_allow_html=True)

st.markdown('<a name="Introduction"></a>', unsafe_allow_html=True)
st.markdown("""
## Introduction to Basics

Dynamic models of controlled systems are often developed based on experimental studies of the system’s response to a 
step input.
This experimental method for determining the dynamic characteristics of an industrial system involves recording the step 
response curve (the experimental transient function) and approximating it with the solution of a linear differential 
equation with constant coefficients.
To calculate the controller tuning parameters for the designed automatic control system (ACS), the transfer function of 
the process with respect to the control input is required.

---
""")

st.markdown('<a name="Object"></a>', unsafe_allow_html=True)
st.markdown("""## Object Models
In many cases, the dynamic properties of industrial processes can be represented with sufficient accuracy using 
the following models:""")

st.latex(r"""
\begin{array}{|c|c|c|}
\hline
\textbf{Object order} & \textbf{Object equations} & \textbf{Transfer functions} \\
\hline
\text{1st} & T_{ob}\frac{dy}{dt} + y(t) = k_{ob} \cdot x(t) & W_{ob}(s) = \frac{k_{ob}}{T_{ob}s + 1} \\
\hline
\text{1st with delay} & T_{ob}\frac{dy}{dt} + y(t) = k_{ob} \cdot x(t - \tau_{ob}) & W_{ob}(s) = \frac{k_{ob}}{T_{ob}s + 1} e^{-\tau_{ob}s} \\
\hline
\text{2nd} & T_{ob1}T_{ob2}\frac{d^2y}{dt^2} + (T_{ob1}+T_{ob2})\frac{dy}{dt} + y(t) = k_{ob} \cdot x(t) & W_{ob}(s) = \frac{k_{ob}}{(T_{ob1}s+1)(T_{ob2}s+1)} \\
\hline
\text{2nd with delay} & T_{ob1}T_{ob2}\frac{d^2y}{dt^2} + (T_{ob1}+T_{ob2})\frac{dy}{dt} + y(t) = k_{ob} \cdot x(t - \tau_{ob}) & W_{ob}(s) = \frac{k_{ob}}{(T_{ob1}s+1)(T_{ob2}s+1)} e^{-\tau_{ob}s} \\
\hline
\end{array}
""")
st.markdown("---")

st.markdown('<a name="PID_Basics"></a>', unsafe_allow_html=True)
st.markdown("""
## PID Basics
Proportional–Integral–Derivative (PID) control is one of the most widely used methods in automation and control 
engineering.  
It generates a control signal based on the difference between the desired setpoint and the measured process value.  
This difference is called the **error** (*e(t)*).  
""")

st.markdown('<a name="Forms"></a>', unsafe_allow_html=True)
st.markdown("### PID forms")
st.markdown("""There are two common mathematical forms of PID controllers: **standard** and **parallel**.""")
st.markdown("#### Standard Form")
st.latex(r"u(t) = K \left( e(t) + \frac{1}{T_i} \int_0^t e(t)\, dt + T_d \frac{de(t)}{dt} \right)")

st.markdown("#### Parallel Form")
st.latex(r"u(t) = K_p e(t) + K_i \int_0^t e(t)\, dt + K_d \frac{de(t)}{dt}")

st.markdown("""
- **Proportional (P):** Reacts to the current error. Improves response speed, but excessive values may cause 
instability.  
- **Integral (I):** Accumulates past error. Eliminates steady-state offset, but too much can lead to oscillations.  
- **Derivative (D):** Predicts future error by using its rate of change. Improves damping and stability, but sensitive 
to noise.  

#### Differences Between Forms

- **Standard form:**  
  Uses **one overall gain** with time constants.  
  Often found in theoretical descriptions and in some academic materials.  

- **Parallel form:**  
  Uses **three separate gains**.  
  It is intuitive and widely used in software implementations because each term is tuned independently.  

#### Practical Use

- **Parallel**: preferred in digital controllers and tuning software.
- **Series**: used mainly in hardware or analog circuits, where filters are implemented sequentially.
- **Standard**: primarily theoretical, often used in simplified models.

This application allows you to work with these forms and calculate PID coefficients for your specific needs.

""")

st.markdown('<a name="Math_forms"></a>', unsafe_allow_html=True)
st.markdown("### Mathematical Description of Ideal Controllers")

st.latex(r"""
\begin{array}{|c|c|c|}
\hline
\textbf{Type} & \textbf{Equation of ideal controller} & \textbf{Transfer function} \\
\hline
\text{I} & r(t) = \frac{k_R}{T_i} \int_0^t e(t)\, dt & W_I(s) = \frac{k_R}{T_i s} \\
\hline
\text{P} & r(t) = k_R \cdot e(t) & W_P(s) = k_R \\
\hline
\text{PI} & r(t) = k_R \left[ e(t) + \frac{1}{T_i}\int_0^t e(t)\, dt \right] & W_{PI}(s) = k_R \frac{T_i s + 1}{T_i s} \\
\hline
\text{PID} & r(t) = k_R \left[ e(t) + \frac{1}{T_i}\int_0^t e(t)\, dt + T_d \frac{de(t)}{dt} \right] & W_{PID}(s) = k_R 
\frac{T_i T_d s^2 + T_i s + 1}{T_i s} \\
\hline
\end{array}
""")

st.markdown('<a name="DCS"></a>', unsafe_allow_html=True)
st.markdown("### PID in various DCS")

st.markdown("### Yokogawa (CentumVP, CS3000) PID Controller")

st.latex(r"""
u(t) = \frac{100}{P} \times \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \cdot \frac{de(t)}{dt} \right)
""")

st.markdown("""
**Where:**  
- **u(t)** = Controller Output  
- **e(t)** = Error = SP – PV  
- **P** = Proportional Band [%], relation: $K_c = \\frac{100}{P}$  
- **I** = Reset Time [s]  
- **D** = Derivative Time [s]  
""")

st.markdown("### Siemens (SIMATIC PCS7, S7 PID FB)")

st.latex(r"""
u(t) = P \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \cdot \frac{de(t)}{dt} \right)
""")

st.markdown("""
**Where:**  
- **u(t)** = Controller Output  
- **e(t)** = SP – PV  
- **P** = Proportional Gain (inverse of PB)  
- **I** = Integral (Reset) Time [s]  
- **D** = Derivative Time [s]  
""")

st.markdown("### Honeywell (TDC3000, Experion PKS)")

st.latex(r"""
u(t) = P \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \cdot \frac{de(t)}{dt} \right)
""")

st.markdown("""
**Where:**  
- **u(t)** = Controller Output  
- **e(t)** = SP – PV  
- **P** = Controller Gain (direct, not PB)  
- **I** = Reset Time [s]  
- **D** = Derivative Time [s]  
""")

st.markdown("### Emerson (DeltaV, Ovation)")

st.latex(r"""
u(t) = P \cdot e(t) + \frac{P}{I}\int e(t)\,dt + P D \cdot \frac{de(t)}{dt}
""")

st.markdown("""
**Where:**  
- **u(t)** = Controller Output  
- **e(t)** = SP – PV  
- **P** = Controller Gain  
- **I** = Integral Time [s]  
- **D** = Derivative Time [s]  
""")

st.markdown("### ABB (800xA, Freelance)")

st.latex(r"""
u(t) = P \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \frac{de(t)}{dt} \right)
""")

st.markdown("""
**Where:**  
- **u(t)** = Controller Output  
- **e(t)** = SP – PV  
- **P** = Proportional Gain  
- **I** = Integral Time [s]  
- **D** = Derivative Time [s]  
""")

st.markdown("""
The task of synthesizing an automatic control system consists of selecting a control law and calculating its 
coefficients to ensure the required control quality while maintaining operability.  
The solution to this problem is not unique and depends on the chosen criterion for evaluating control quality.  

In engineering practice, a wide range of methods are used to calculate the tuning parameters of typical industrial 
controllers. Some of them are listed below:

1. Method based on the "optimal modulus" criterion [1]
2. Method based on the "aperiodic stability" criterion [1]
3. Coon's method [2]
4. Kopelovich's method [3]
5. Kopelovich–Sharkov method [4;5]
6. Method based on the "maximum stability" criterion [6]
7. Ziegler–Nichols method [7]
8. Huang method [7]
9. AMIGO method [8]
10. Lambda Tuning [8]
11. Skogestad's method [9]

---
""")

st.markdown('<a name="Loading"></a>', unsafe_allow_html=True)
st.markdown("""
## Data Loading
### The Data loading section helps you upload and preprocess your historical data.

You can upload files up to 200 MB each via drag-and-drop or by using the 'Browse files' button.  
This application supports only .csv files!""")

st.image("pics/data_loading.png", caption="Data Loading")

st.markdown("""
If your file is larger than 200 MB you can select the corresponding checkbox.
This action will scan the application's root directory and display a dropdown list of available .csv files.
""")

st.image("pics/data_loading_2.png", caption="Data Loading 2")

st.markdown("""
After selecting the data file, you will see the data file settings.  
You can choose column separator:
- semicolon ;
- comma ,
- dot .
- tab   

and decimal separator:
- comma ,
- full stop .

Then you can choose the row that contains the headers of columns and optionally skip rows or columns if they are present 
in data.
""")
st.image("pics/separators.png", caption="Selecting separators")

st.markdown("""
Then choose a datetime format from dropdown list or select "No datetime column".
If selected, you can set the time interval and the start date and time.
""")

st.image("pics/datetime.png", caption="Datetime")

st.markdown("""
If you want to preview your data before processing, check the "Data preview" box to display the first 5 rows.

---
""")

st.markdown('<a name="Fitting"></a>', unsafe_allow_html=True)
st.markdown("""
## Model Fitting
### Model Fitting section helps you convert your historical data into a process model and obtain its parameters
First, you need to choose the Manipulated Variable (MV) and Process Variable (PV).
- **Manipulated variable** is valve position percentage % - variable you change to get response (process input).
- **Process variable** is the current measured process value - response from the input change (process output).

Tick "Show linechart" to check your data.

Then you can select the model order using dropdown list.
""")

st.image("pics/MV_PV_order.png", caption="Model Fitting")

st.markdown("""
The program will automatically calculate all coefficients. You can then manually adjust them using sliders or 
by entering the required values.

ΔMV is a step input in your data. Kob, τob, Tob are object [model](#Object) coefficients.
""")

st.image("pics/coefficients.png", caption="Model Coefficients")

st.markdown("""
After that, a chart with your process model and its parameters will be displayed below.
""")

st.image("pics/object_parameters.png", caption="Object Parameters")

st.markdown("""
---
""")

st.markdown('<a name="Tuning"></a>', unsafe_allow_html=True)
st.markdown("""
## PID Tuning
### PID Tuning section helps you obtain parameters for the PID controller

First, you need to choose PID type (PI/PID).  
Then choose one of the available methods from the dropdown list. The available methods depend on the selected model 
order and PID type.  
Finally, select the PID form you need. The corresponding equation will appear below to help ensure correct selection.  
PID parameters will appear below.  
""")

st.image("pics/pid_tuning.png", caption="PID Tuning")

st.markdown("""
---
""")
st.markdown('<a name="References"></a>', unsafe_allow_html=True)
st.markdown("## References")

st.markdown("""
1. Guretsky, H. (1974). *Analysis and Synthesis of Control Systems with Delay*. Moscow: Mashinostroenie.  
2. Shteinberg, Sh. E., et al. (1973). *Industrial Automatic Regulators*. Moscow: Energiya.  
3. Dubrovny, V. A., et al. (1981). *Handbook on Adjustment of Automatic Control and Regulation Devices* (Part 2). Kiev: Naukova Dumka.  
4. Sharkov, A. A., et al. (1990). *Automatic Control and Regulators in the Chemical Industry*. Moscow: Khimiya.  
5. Ginzburg, I. B. (1985). *Automatic Control and Regulators in the Building Materials Industry*. Leningrad: Stroyizdat.  
6. Zagriy, G. I., & Shublandze, A. M. (1988). *Synthesis of Control Systems Based on the Maximum Stability Degree Criterion*. Moscow: Energoizdat.  
7. O’Dwyer, A. (2009). *Handbook of PI and PID Controller Tuning Rules* (3rd ed.). London: Imperial College Press.  
8. Åström, K. J., & Hägglund, T. (2006). *Advanced PID Control*. ISA – The Instrumentation, Systems, and Automation Society.  
9. Skogestad, S. (2003). Simple analytic rules for model reduction and PID controller tuning. *Journal of Process Control*, 13, 291–309.  
""")

st.markdown("""
## Disclaimer
This software is provided "as is" for educational and informational purposes only.
The author makes no representations or warranties of any kind, express or implied, regarding the accuracy, reliability, 
or suitability of the PID tuning parameters or recommendations generated by this application.
Any use of this software, including applying its output to real-world systems or processes, is at your own risk.
The author shall not be held liable for any direct, indirect, incidental, or consequential damages, losses, or costs 
resulting from the use, misuse, or inability to use this software or its recommendations.""")

st.markdown("### Created by [NosterDream](https://github.com/nosterdream)")
