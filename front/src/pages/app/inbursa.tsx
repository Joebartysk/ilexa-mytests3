import { CONFIG } from 'src/config-global';

import { InbursaView } from 'src/sections/app-sections/inbursa/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Estados de Cuenta-Inbursa  - ${CONFIG.appName}`}</title>

			<InbursaView />
		</>
	);
}
