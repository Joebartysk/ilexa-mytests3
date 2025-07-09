import { CONFIG } from 'src/config-global';

import { NolocalizableView } from 'src/sections/app-sections/nolocalizable/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`RFCs No localizables - ${CONFIG.appName}`}</title>

			<NolocalizableView />
		</>
	);
}
