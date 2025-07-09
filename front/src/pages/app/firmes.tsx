import { CONFIG } from 'src/config-global';

import { FirmesView } from 'src/sections/app-sections/firmes/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`RFCs Firmes - ${CONFIG.appName}`}</title>

			<FirmesView />
		</>
	);
}
