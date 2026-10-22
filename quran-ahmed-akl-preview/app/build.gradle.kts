plugins {
    id("com.android.application")
}

android {
    namespace = "com.baraemest.quranahmedakl.preview"
    compileSdk = 35
    defaultConfig {
        applicationId = "com.baraemest.quranakl.duo.fixed"
        minSdk = 24
        targetSdk = 35
        versionCode = 3
        versionName = "1.2-test"
    }
    buildTypes {
        getByName("release") { isMinifyEnabled = false }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}
