import { CONFIG } from 'src/config-global';

import { MetodoPagoView } from 'src/sections/app-sections/metodopago/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Metodo Pago - ${CONFIG.appName}`}</title>

			<MetodoPagoView />
		</>
	);
}
