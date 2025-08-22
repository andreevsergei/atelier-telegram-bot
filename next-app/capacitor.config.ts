import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
	appId: 'com.example.nextapp',
	appName: 'Next App',
	webDir: 'out',
	bundledWebRuntime: false,
	server: {
		androidScheme: 'https'
	}
};

export default config;