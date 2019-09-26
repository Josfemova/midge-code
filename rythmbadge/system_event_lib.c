#include "system_event_lib.h"

#include "nrf_sdh.h"
#include "nrf_sdh_soc.h"


static volatile system_event_handler_t event_handlers[MAX_NUMBER_SYSTEM_EVENT_HANDLER];	/**< Array to save the application system event handlers that are called when a system event is generated. */
static volatile uint32_t number_system_event_handler = 0;								/**< Number of registered application system event handlers. */



/**@brief Internal system event callback for calling the registered application system event handlers.
 *
 * @param[in]	sys_evt		The generated system_event that should be transfered to the application system event handlers.
 */
static void system_event_dispatch(uint32_t evt_id, void * p_context)
{	
	// Call all the registered event handlers
	for(uint32_t i = 0; i < number_system_event_handler; i++){
		event_handlers[i](evt_id, p_context);
	}
}


#define APP_SOC_OBSERVER_PRIO	1	// Max is 2 in config


void system_event_init(void) {
	// Only initialize the module once!
	static uint8_t init_done = 0;
	if(init_done == 0) {
		// Register with the SoftDevice handler module for system events.
//		uint32_t err_code = softdevice_sys_evt_handler_set(system_event_dispatch);
		NRF_SDH_SOC_OBSERVER(m_soc_observer, APP_SOC_OBSERVER_PRIO, system_event_dispatch, NULL);
		
//		(void)(err_code);
		//APP_ERROR_CHECK(err_code);
		
		number_system_event_handler = 0;
		init_done = 1;
	}
}




ret_code_t system_event_register_handler(system_event_handler_t event_handler) {
	if(number_system_event_handler >= MAX_NUMBER_SYSTEM_EVENT_HANDLER) {
		return NRF_ERROR_NO_MEM;
	}
	
	event_handlers[number_system_event_handler] = event_handler;
	number_system_event_handler++;
	
	return NRF_SUCCESS;
}
