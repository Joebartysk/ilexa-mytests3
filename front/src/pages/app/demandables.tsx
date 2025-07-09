import { CONFIG } from 'src/config-global';

import { DemandablesView } from 'src/sections/app-sections/demandables/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`RFCs Demandables - ${CONFIG.appName}`}</title>

			<DemandablesView />
		</>
	);
}
