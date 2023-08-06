package {{%site%}};

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import pub.devrel.easypermissions.EasyPermissions;

public class {{%name%}} extends Activity implements EasyPermissions.PermissionCallbacks,
        EasyPermissions.RationaleCallbacks {
    PyObject pa = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //------------------检测是否已经初始化Python环境------------------
        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }
        //初始化，为APP赋值
        Python python = Python.getInstance();
        PyObject pyObject = python.getModule("main");
        PyObject PyAPP = pyObject.callAttr("MainAPP");
        //---------------------检测启动的Activity-----------------------
        //获取Intent，查看是否有前置消息
        Intent intent = getIntent();
        String activity_info = intent.getStringExtra("new_activity");

        PyObject python_central_activity;
        //如果携带信息不为空，证明这是启动的新的Activity，则根据信息去查找对应的Activity并启动
        if (activity_info != null) {
            python_central_activity = PyAPP.callAttr("get_target_activity", activity_info);
            python_central_activity.callAttr("External_assignment_Activity", this);
            python_central_activity.callAttr("External_assignment_intent", intent);
            PyAPP.callAttr("bind_activity", activity_info);
        } else {
            //否则，如果是空的，证明这是第一次启动，则不进行任何判断
            python_central_activity = PyAPP.get("now_activity");
            assert python_central_activity != null;
            python_central_activity.callAttr("External_assignment_Activity", this);
            python_central_activity.callAttr("External_assignment_intent", intent);
        }
        this.pa = python_central_activity;
        this.pa.callAttr("External_assignment_sensor_manager", getSystemService(Context.SENSOR_SERVICE));
        this.pa.callAttr("External_assignment_location_manager", getSystemService(Context.LOCATION_SERVICE));
        this.pa.callAttr("External_assignment_notification_manager", getSystemService(Context.NOTIFICATION_SERVICE));
        // ----------------==为中央控制器中的R文件赋值======================

        Class R_attrs[] = R.class.getDeclaredClasses();
        for (Class a : R_attrs) {
            String sourse_type = a.getName();
            Map<String, Integer> attr_map = new HashMap<>();
            Field[] fields = a.getDeclaredFields();
            for (Field field : fields) {
                try {
                    attr_map.put(field.getName(), field.getInt(null));
                } catch (IllegalAccessException e) {
                    e.printStackTrace();
                }
            }
            python_central_activity.callAttr("External_assignment_R", attr_map, sourse_type);
        }
        // ------------------======================
        python_central_activity.callAttr("onCreate", savedInstanceState);

        //-------------

    }

    @Override
    protected void onPause() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onPause")).toBoolean()) {
            super.onPause();
        }
        this.pa.callAttr("onPause");
    }

    @Override
    protected void onStart() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onStart")).toBoolean()) {
            super.onStart();
        }
        this.pa.callAttr("onStart");
    }

    @Override
    protected void onStop() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onStop")).toBoolean()) {
            super.onStop();
        }
        this.pa.callAttr("onStop");
    }

    @Override
    protected void onDestroy() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onDestroy")).toBoolean()) {

            super.onDestroy();
        }
        this.pa.callAttr("onDestroy");
    }

    @Override
    protected void onRestart() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onRestart")).toBoolean()) {

            super.onRestart();
        }
        this.pa.callAttr("onRestart");
    }

    @Override
    protected void onResume() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onResume")).toBoolean()) {

            super.onResume();
        }
        this.pa.callAttr("onResume");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onActivityResult")).toBoolean()) {

            super.onActivityResult(requestCode, resultCode, data);
        }
        this.pa.callAttr("onActivityResult", requestCode, resultCode, data);
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onConfigurationChanged")).toBoolean()) {

            super.onConfigurationChanged(newConfig);
        }
        this.pa.callAttr("onConfigurationChanged", newConfig);
    }

    @Override
    public void onBackPressed() {
        if (Objects.requireNonNull(Objects.requireNonNull(this.pa.get("if_call_super")).asMap().get("onBackPressed")).toBoolean()) {

            super.onBackPressed();
        }
        this.pa.callAttr("onBackPressed");
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        EasyPermissions.onRequestPermissionsResult(requestCode, permissions, grantResults, this);
    }

    @Override
    public void onPermissionsGranted(int requestCode, @NonNull List<String> perms) {
        //权限成功赋予
        this.pa.callAttr("onPermissionsGranted", requestCode, perms);
    }

    @Override
    public void onPermissionsDenied(int requestCode, @NonNull List<String> perms) {
        //权限被拒绝
        this.pa.callAttr("onPermissionsDenied", requestCode, perms);
    }

    @Override
    public void onRationaleAccepted(int requestCode) {
        this.pa.callAttr("onRationaleAccepted", requestCode);
    }

    @Override
    public void onRationaleDenied(int requestCode) {
        this.pa.callAttr("onRationaleDenied", requestCode);
    }

    //-------------------------事件回调---------------------------------
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        return super.onKeyDown(keyCode, event);
    }

    @Override
    public boolean onKeyLongPress(int keyCode, KeyEvent event) {
        return super.onKeyLongPress(keyCode, event);
    }

    @Override
    public boolean onKeyShortcut(int keyCode, KeyEvent event) {
        return super.onKeyShortcut(keyCode, event);
    }

    @Override
    public boolean onKeyUp(int keyCode, KeyEvent event) {
        return super.onKeyUp(keyCode, event);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        return super.onTouchEvent(event);
    }

    @Override
    public boolean onTrackballEvent(MotionEvent event) {
        return super.onTrackballEvent(event);
    }
    // -----------------------------END-事件回调-----------------------------
}