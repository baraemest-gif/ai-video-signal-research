plugins {
    id("com.android.application")
}

android {
    namespace = "com.baraemest.quranahmedakl.preview"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.baraemest.quranahmedakl.preview"
        minSdk = 24
        targetSdk = 35
        versionCode = 1
        versionName = "1.0-test"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
