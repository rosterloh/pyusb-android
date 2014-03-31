/**
 *
 * @author      Manuel Di Cerbo
 * @copyright   Copyright (c) 2013, Manuel Di Cerbo, Nexus-Computing GmbH
 *
 * This file is part of SimpleAccessory.
 *
 * SimpleAccessory is free software; you can redistribute it and/or modify it under
 * the terms of the GNU General Public License version 2, as published by the
 * Free Software Foundation.
 *
 * You may NOT assume that you can use any other version of the GPL.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details
 *
 * You should have received a copy of the GNU General Public License along with
 * this program; if not, write to:
 *
 *      Free Software Foundation, Inc.
 *      51 Franklin St, Fifth Floor
 *      Boston, MA  02110-1301  USA
 *
 * The license for this software can also likely be found here:
 * http://www.gnu.org/licenses/gpl-2.0.html
 */

package ch.nexuscomputing.simpleaccessory;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.WindowManager;
import android.widget.SeekBar;
import android.widget.SeekBar.OnSeekBarChangeListener;
import ch.nexuscomputing.simpleaccessory.AccessoryEngine.IEngineCallback;

/**
 * @author mdc
 *
 */
public class MainActivity extends Activity {

	private SeekBar mBrightnessBar;
	private AccessoryEngine mEngine = null;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
		onNewIntent(getIntent());
		setContentView(R.layout.activity_main);
		mBrightnessBar = (SeekBar) findViewById(R.id.sbBrightness);
		mBrightnessBar.setOnSeekBarChangeListener(mSeekBarListener);

	}

	@Override
	protected void onNewIntent(Intent intent) {
		L.d("handling intent action: " + intent.getAction());
		if (mEngine == null) {
			mEngine = new AccessoryEngine(getApplicationContext(), mCallback);
		}
		mEngine.onNewIntent(intent);
		super.onNewIntent(intent);
	}

	@Override
	protected void onDestroy() {
		mEngine.onDestroy();
		mEngine = null;
		super.onDestroy();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	private final OnSeekBarChangeListener mSeekBarListener = new OnSeekBarChangeListener() {
		@Override
		public void onStopTrackingTouch(SeekBar seekBar) {
		}

		@Override
		public void onStartTrackingTouch(SeekBar seekBar) {
		}

		@Override
		public void onProgressChanged(SeekBar seekBar, int progress,
				boolean fromUser) {
			L.d("value is %d", progress);
			if (fromUser && mEngine != null) {
				mEngine.write(new byte[] { (byte) progress });
			}
		}
	};

	private final IEngineCallback mCallback = new IEngineCallback() {
		@Override
		public void onDeviceDisconnected() {
			L.d("device physically disconnected");
		}

		@Override
		public void onConnectionEstablished() {
			L.d("device connected! ready to go!");
		}

		@Override
		public void onConnectionClosed() {
			L.d("connection closed");
		}

		@Override
		public void onDataRecieved(byte[] data, int num) {
			L.d("received %d bytes", num);
		}
	};

}
