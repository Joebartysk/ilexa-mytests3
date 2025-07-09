import { CONFIG } from 'src/config-global';

import { ClaveProdServView } from 'src/sections/app-sections/claveprodserv/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Clave Producto-Servicio  - ${CONFIG.appName}`}</title>

			<ClaveProdServView />
		</>
	);
}
