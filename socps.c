#include "contiki.h" //Imports
#include <stdio.h>
#include <random.h>

PROCESS(bpm, "Batimentos Cardiacos"); // Definindo processos
PROCESS(saturacao, "Saturacao");
PROCESS(febre, "Febre");
PROCESS(display_process, "Febre");


AUTOSTART_PROCESSES(&bpm, &saturacao, &febre, &display_process); //Startando processos

PROCESS_THREAD(bpm, ev, data)
{
  static struct etimer timer;

  PROCESS_BEGIN();

  etimer_set(&timer, CLOCK_SECOND * 3); //Tempo para qual o processo vai rodar

  static char msg[50];

  int numero = 0;
  
  while(true) {

    numero = 20 + random_rand() % (140 - 20); //Definindo o valor aleatorio para os batimentos
    if (numero > 90) { //Validacoes
      sprintf(msg,"BPM elevado:  %d\n",numero);
      process_post(&display_process,PROCESS_EVENT_MSG,&msg); //Chamado do processo para exibir a mensagem do alerta
    } else if (numero < 50) {
      sprintf(msg,"BPM abaixo do esperado:  %d\n",numero);
      process_post(&display_process,PROCESS_EVENT_MSG,&msg);
    } else {
      sprintf(msg,"BPM Normal:  %d\n",numero);
    }
    
    
    printf("%s",msg);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
    etimer_reset(&timer);

  }
  PROCESS_END();
}

PROCESS_THREAD(saturacao, ev, data)
{
  static struct etimer timer;

  PROCESS_BEGIN();

  etimer_set(&timer, CLOCK_SECOND * 3);

  int numero = 0;

  static char msg[50];

  while(true) {

    numero = 80 + random_rand() % (100 - 80);
    if (numero < 90) {
      sprintf(msg,"Saturacao abaixo do esperado:  %d\n",numero);
      process_post(&display_process,PROCESS_EVENT_MSG,&msg);
    } else {
      sprintf(msg,"Saturacao Normal:  %d\n",numero);
    }
    
    printf("%s",msg);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
    etimer_reset(&timer);

  }
  PROCESS_END();
}

PROCESS_THREAD(febre, ev, data)
{
  static struct etimer timer;

  PROCESS_BEGIN();

  etimer_set(&timer, CLOCK_SECOND * 3);

  int numero = 0;

  static char msg[50];

  while(true) {

    numero = 34 + random_rand() % (41 - 34);
    if (numero < 35) {
      sprintf(msg,"Hiportemia, Temp:  %d\n",numero);
      process_post(&display_process,PROCESS_EVENT_MSG,&msg);
    } else if (numero > 37) {
      sprintf(msg,"Febre, Temp:  %d\n",numero);
      process_post(&display_process,PROCESS_EVENT_MSG,&msg);
    } else {
      sprintf(msg,"Temp Normal:  %d\n",numero);
    }
    
    printf("%s",msg);

    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
    etimer_reset(&timer);

  }
  PROCESS_END();
}

PROCESS_THREAD(display_process, ev, data)
{

  PROCESS_BEGIN();

  while(true) {
    
    PROCESS_WAIT_EVENT(); //Processo aguarda chamada feita quando um dado esta fora do normal

    if(PROCESS_EVENT_MSG == ev){
    	printf("ALERTA - %s\n", (char*)data); //Exibindo a mensagem de alerta recebida
    }

  }

  PROCESS_END();
}
