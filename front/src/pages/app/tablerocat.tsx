import { CONFIG } from 'src/config-global';

import { TablerocatView } from 'src/sections/app-sections/tablerocat/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Catalogos  - ${CONFIG.appName}`}</title>

			<TablerocatView />
		</>
	);
}
