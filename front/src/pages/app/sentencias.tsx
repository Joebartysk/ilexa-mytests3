import { CONFIG } from 'src/config-global';

import { SentenciasView } from 'src/sections/app-sections/sentencias/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Sentencias  - ${CONFIG.appName}`}</title>

			<SentenciasView />
		</>
	);
}
