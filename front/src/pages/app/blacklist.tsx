import { CONFIG } from 'src/config-global';

import { BlacklistView } from 'src/sections/app-sections/blacklist/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Listas negras  - ${CONFIG.appName}`}</title>

			<BlacklistView />
		</>
	);
}
