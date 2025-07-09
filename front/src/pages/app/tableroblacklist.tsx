import { CONFIG } from 'src/config-global';

import { TablerocatView } from 'src/sections/app-sections/tableroblacklist/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Listas EFOs y EDOS  - ${CONFIG.appName}`}</title>

			<TablerocatView />
		</>
	);
}
