import { CONFIG } from 'src/config-global';

import { MesesView } from 'src/sections/app-sections/meses/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Meses  - ${CONFIG.appName}`}</title>

			<MesesView />
		</>
	);
}
