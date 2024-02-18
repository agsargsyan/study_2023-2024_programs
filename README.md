# Имитационная и Натурная модели одинаковой топологии для научно-исследовательской работы

## Описание топологии

Мною был написана программа, реализующая имитационную и натурную модели сети со следующей топологией:

- $N=20$ TCP-источников, $N$ TCP-приёмников, двух маршрутизаторов $R1$
  и $R2$ между источниками и приёмниками ($N$ — не менее 20);
- между TCP-источниками и первым маршрутизатором установлены
  дуплексные соединения с пропускной способностью 100 Мбит/с и
  задержкой 20 мс очередью типа DropTail;
- между TCP-приёмниками и вторым маршрутизатором установлены
  дуплексные соединения с пропускной способностью 100 Мбит/с и
  задержкой 20 мс очередью типа DropTail;
- между маршрутизаторами установлено симплексное соединение
  ($R1$---$R2$) с пропускной способностью 20 Мбит/с и задержкой 15 мс
  очередью типа RED, размером буфера 300 пакетов; в обратную сторону~--- 
  симплексное соединение ($R2$---$R1$) с пропускной способностью 15 Мбит/с и
  задержкой 20 мс очередью типа DropTail;
- данные передаются по протоколу FTP поверх TCPReno;
- параметры алгоритма RED: $q_{\min}=75$, $q_{\max}=150$, $q_w=0,002$, $p_{\max}=0.1$;
- максимальный размер TCP-окна 32; размер передаваемого пакета 500
  байт; время моделирования~---25 единиц модельного времени.


## Описание имитационной модели

Для реализации имитационной модели была использованы сценарии NS-2, для построения графиков используется GNUplot и Xgraph для быстрого просмотра.

В имитационной модели представлены следующие разновидности алгоритма RED 

Модификации, реализованные в NS2
- RED
- GRED
- ARED

Модификации, реализуемые с помощью патчей

- RARED [ссылка на исходный код](https://mohittahiliani.blogspot.com/2012/01/refined-adaptive-red-re-ared-or-rared.html)
- NLRED [ссылка на исходный код](https://mohittahiliani.blogspot.com/2012/01/nonlinear-red-nlred-patch-for-ns-2.html)

Модификации, реализуемые самостоятельно

- Hyperbola RED
- RED-QL
- TRED
- SmRED
- POWARED
- FARED
- DSRED

## Обновленные функции в исходном коде для реализации вариаций

- red.cc 

```
void REDQueue::updateMaxP(double new_ave, double now)
{
	double part = 0.4*(edp_.th_max - edp_.th_min);
	// AIMD rule to keep target Q~1/2(th_min+th_max)
	if ( new_ave < edp_.th_min + part && edv_.cur_max_p > edp_.bottom) {
		// we increase the average queue size, so decrease max_p
		edv_.cur_max_p = edv_.cur_max_p * edp_.beta;
		edv_.lastset = now;
	} else if (new_ave > edp_.th_max - part && edp_.top > edv_.cur_max_p ) {
		// we decrease the average queue size, so increase max_p
		double alpha = edp_.alpha;
                        if ( alpha > 0.25*edv_.cur_max_p )
			alpha = 0.25*edv_.cur_max_p;
		edv_.cur_max_p = edv_.cur_max_p + alpha;
		edv_.lastset = now;
	} 
}

void REDQueue::updateMaxP_refined_adaptive(double new_ave, double now)
{
  	double part = 0.48*(edp_.th_max - edp_.th_min);
 	if ( new_ave < edp_.th_min + part && edv_.cur_max_p > edp_.bottom) {
 		edv_.cur_max_p = edv_.cur_max_p * (1.0 - (0.17 * ((edp_.th_min + part) - new_ave) / ((edp_.th_min + part) - edp_.th_min))); 
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p;
 	} else if (new_ave > edp_.th_max - part && edp_.top > edv_.cur_max_p ) {
 		double alpha = edp_.alpha;
 		alpha = 0.25 * edv_.cur_max_p * ((new_ave - (edp_.th_max - part)) / (edp_.th_max - part));
 		edv_.cur_max_p = edv_.cur_max_p + alpha;
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p;
 	}
}


void REDQueue::updateMaxP_powared(double new_ave, double now)
{
  	double target = 0.5*(edp_.th_max + edp_.th_min);
  	int k = edp_.pwk;
  	int b = edp_.pwb;
  	int r = edp_.bf_size;
  	double v_ave = edv_.v_ave;
  	
  	
  	
  	double delta1 = abs(pow((v_ave - target)/(b * target), k));
  	double delta2 = abs(pow((target - v_ave)/(b * (r -target)), k));
 	
 	if ( new_ave < target && edv_.cur_max_p > edp_.bottom) {
 		edv_.cur_max_p = edv_.cur_max_p - delta1; 
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p; 
 	} else if (new_ave > target && edp_.top > edv_.cur_max_p ) {
 		edv_.cur_max_p = edv_.cur_max_p + delta2;
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p;
 	}
}

void REDQueue::updateMaxP_fast_adaptive(double new_ave, double now){
	  	double part = 0.48*(edp_.th_max - edp_.th_min);
		if ( new_ave < edp_.th_min + part && edv_.cur_max_p > edp_.bottom) {
 		edv_.cur_max_p = edv_.cur_max_p * (1.0 - (0.0385 * ((edp_.th_min + part) - new_ave) / ((edp_.th_min + part) - edp_.th_min))); 
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p;
 	} else if (new_ave > edp_.th_max - part && edp_.top > edv_.cur_max_p ) {
 		double alpha = edp_.alpha;
 		alpha = 0.0412 * edv_.cur_max_p * (new_ave - part) / part;
 		edv_.cur_max_p = edv_.cur_max_p + alpha;
 		edv_.lastset = now;
 		double maxp = edv_.cur_max_p;
 	}


}

double
REDQueue::calculate_p_new(double v_ave, double th_max, int gentle, double v_a, 
	double v_b, double v_c, double v_d, double max_p)
{	
	double target;
	double exponenta = 2.7182818285;
	double th_min = edp_.th_min;
	double p;
	if (gentle && v_ave >= th_max) {
		// p ranges from max_p to 1 as the average queue
		// size ranges from th_max to twice th_max 
		p = v_c * v_ave + v_d;
        } else if (!gentle && v_ave >= th_max) { 
                // OLD: p continues to range linearly above max_p as
                // the average queue size ranges above th_max.
                // NEW: p is set to 1.0 
                p = 1.0;
        } else if (edp_.quadratic_linear == 1) {
        	target = 2 * ((th_min + th_max)/3) - th_min;
        	if(v_ave < target){
        		p = 9 * max_p * ((v_ave-th_min)/(2*(th_max-2*th_min))) * ((v_ave-th_min)/(2*(th_max-2*th_min)));
        	} else if (v_ave >= target) {
        		p = max_p + 3*(1-max_p)*((v_ave-target)/(th_max+th_min));
        	}
        } else if (edp_.improved == 1) {
        	target = ((th_min + th_max)/3) + th_min;
        	if(v_ave < target){
        		p = 9 * max_p * ((v_ave-th_min)/(th_max + th_min)) * ((v_ave-th_min)/(th_max + th_min));
        	} else if (v_ave >= target) {
        		p = max_p + 3*(1-max_p)*(v_ave-target)/(2*(th_max - 2 * th_min));
        	}
        } else if (edp_.smart == 1) {
        	target = ((th_max - th_min)/2) + th_min;
        	if(v_ave < target){
        		p = max_p * pow(((v_ave-th_min)/(th_max - th_min)), 2);
        	} else if (v_ave >= target) {
        		p = max_p * pow(((v_ave-th_min)/(th_max - th_min)), 0.5);
        	}
        } else if (edp_.three_sections == 1){
        	double delta = (th_min+th_max/3);
        	if (v_ave < (th_min + delta)){
        		p = 9 * max_p * pow((v_ave-th_min)/(th_max-th_min), 3) ;
        		}
        	else if ((v_ave >= th_min + delta) && (v_ave < th_min + 2 * delta)){
        		p = max_p * (v_ave-th_min)/(th_max-th_min);
        		}
        	else if (v_ave >= th_min + 2* delta){
        		p =  9 * max_p * pow((v_ave-th_min)/(th_max-th_min), 3) + max_p;
        	} 
        }
        else if (edp_.double_slope == 1) {
        	double a = (2-2* edp_.omega)/(th_max - th_min);
        	double b = (2 * edp_.omega)/(th_max - th_min);
        	target = ((th_max + th_min)/2);
        	if(v_ave < target){
        		p = a * (v_ave-th_min);
        	} else if (v_ave >= target) {
        		p = 1 - edp_.omega + b * (v_ave - target);
        	}
        }
        else {
                // p ranges from 0 to max_p as the average queue
                // size ranges from th_min to th_max 
                p = v_a * v_ave + v_b;
                // p = (v_ave - th_min) / (th_max - th_min)
                
                /* Added by Mohit P. Tahiliani for Nonlinear RED (NLRED) - Start */
				if(edp_.nonlinear == 1){
					p *= p;		// This ensures probability is a quadratic function of "average queue size" as specified in NLRED Paper
				}
				else if (edp_.hyperbola == 1){
					p *= 1/p;	// This ensures probability is a hyperbola function of "average queue size" as specified in HRED Paper
				}
				else if (edp_.exponential == 1){ // Used for RED_e
					p = (pow(exponenta, v_ave)-pow(exponenta, th_min))/(pow(exponenta, th_max)-pow(exponenta, th_min));
				}
                p *= max_p; 
        }
	if (p > 1.0)
		p = 1.0;
	return p;
}
```

- red.h

```
	int feng_adaptive;	/* adaptive RED: Use the Feng et al. version */
	int refined_adaptive;	/* Added by Mohit P. Tahiliani for Refined Adaptive RED (Re-ARED) */
	int stabilized_adaptive;/* Added Stabillized Adaptive RED (SARED) */
	int nonlinear;		/* Added for Nonlinear RED (NLRED) */
	int hyperbola;		/* Added for Hyperbola RED (HRED)*/
	int quadratic_linear;   /* Added for Quadratic linear RED*/
	int three_sections;	/* Added for 3sections RED*/
	int exponential;	/* Added for exponential RED*/
	int improved;		/* Added for improved RED*/
	int smart;		/* Added for smart RED*/
	int modified;		/* Added for modified RED*/	 
```

- ns-default.tcl
 
```
/*Added for new RED alghorithms*/

Queue/RED set nonlinear_ 0
Queue/RED set hyperbola_ 0
Queue/RED set quadratic_linear_ 0
Queue/RED set three_sections_ 0
Queue/RED set exponential_ 0
Queue/RED set improved_ 0
Queue/RED set smart_ 0
Queue/RED set modified_ 0
```

Для смены модификации нужно расскоментировать выбор в файле ns-2/queue.tcl репозитория и закомментировать предыдущую вариацию, для вариаций адаптивных алгоритмов расскоментировать и классическую адаптивную версию.


## Натурная модель 
 
В mininet, в отличие от NS-2, используются реальные виртуальные устройства. Маршрутизаторы r0 и r1 реализованы с помощью класса LinuxRouter, оконечные устройства подключены к маршрутизаторам с помощью коммутаторов s1 и s2. Для моделирования использована утилита iperf3 с помощью паралельных потоков, где устройства, подключенные к r1 являются серверами, а устройства, подключенные к r0, клиентами.
Все данные на каждый источник выводятся в файлы формата .json с помощью команды plot_iperf.sh [репозиторий](https://github.com/ekfoury/iperf3_plotter), которые с помощью скрипта all.py собираются в один файл для постройки графика метрик cwnd, rtt и rtt_var для всех источников.

Алгоритм RED использован с помощью linux traffic control, параметры настроены в байтах аналогично данным в NS-2. Возникла проблема с тем, что в iperf3 и mininet нет возможноасти для настройки параметра maxcwnd. 





 
 
