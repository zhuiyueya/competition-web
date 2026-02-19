<script>
export default {
  onLaunch() {
    try {
      const cur = String(uni.getStorageSync('base_url') || '').trim()
      if (!cur) {
        uni.setStorageSync('base_url', 'http://192.168.0.136:5000')
      }
    } catch (e) {}
  },
  onShow() {
  },
  onHide() {
  }
}
</script>

<style>
</style>
