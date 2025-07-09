import { CONFIG } from 'src/config-global';

import { FormaPagoView } from 'src/sections/app-sections/formapago/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Forma Pago - ${CONFIG.appName}`}</title>

			<FormaPagoView />
		</>
	);
}
