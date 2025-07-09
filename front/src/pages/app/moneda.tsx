import { CONFIG } from 'src/config-global';

import { MonedaView } from 'src/sections/app-sections/moneda/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Moneda - ${CONFIG.appName}`}</title>

			<MonedaView />
		</>
	);
}
