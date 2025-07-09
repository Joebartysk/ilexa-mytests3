import { CONFIG } from 'src/config-global';

import { BBVAView } from 'src/sections/app-sections/bbva/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Estados de Cuenta-BBVA  - ${CONFIG.appName}`}</title>

			<BBVAView />
		</>
	);
}
