import { CONFIG } from 'src/config-global';

import { ObjetoImpView } from 'src/sections/app-sections/objetoimp/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Objeto Impuesto - ${CONFIG.appName}`}</title>

			<ObjetoImpView />
		</>
	);
}
