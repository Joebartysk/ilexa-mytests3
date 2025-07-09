import { CONFIG } from 'src/config-global';

import { TasaOCuotaView } from 'src/sections/app-sections/tasaocuota/view';

// ----------------------------------------------------------------------

export default function Page() {
	return (
		<>
			<title>{`Tasa o Cuota  - ${CONFIG.appName}`}</title>

			<TasaOCuotaView />
		</>
	);
}
