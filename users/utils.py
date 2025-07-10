def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

#'user_5/avatar.png'  # for example, if user.id = 5 and file name is avatar.png. Simply {0}  = instance.user.id and {1} = filename
   